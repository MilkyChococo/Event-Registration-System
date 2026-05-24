import {
  api,
  escapeHtml,
  formatCurrency,
  formatDateTime,
  getCurrentUser,
  redirectTo,
  renderUserAvatar,
  setupAccountMenu,
  setupGlobalFooter,
} from "/static/shared.js?v=20260406-contact-stack-fab";

const reservationAvatar = document.querySelector("[data-testid='reservation-avatar']");
const reservationTitle = document.querySelector("#reservation-title");
const reservationHeroCopy = document.querySelector("#reservation-hero-copy");
const reservationWelcomeText = document.querySelector("#reservation-welcome-text");
const reservationRoleChip = document.querySelector("#reservation-role-chip");
const reservationAdminTopbarNav = document.querySelector("#reservation-admin-topbar-nav");
const reservationJoinedCount = document.querySelector("#reservation-joined-count");
const reservationActiveCount = document.querySelector("#reservation-active-count");
const reservationTicketCount = document.querySelector("#reservation-ticket-count");
const reservationList = document.querySelector("#reservation-list");
const reservationTicketModal = document.querySelector("#reservation-ticket-modal");
const reservationTicketTitle = document.querySelector("#reservation-ticket-title-heading");
const reservationTicketCode = document.querySelector("#reservation-ticket-code");
const reservationTicketStatus = document.querySelector("#reservation-ticket-status");
const reservationTicketSummary = document.querySelector("#reservation-ticket-summary");
const reservationTicketMeta = document.querySelector("#reservation-ticket-meta");
const reservationTicketQrImage = document.querySelector("#reservation-ticket-qr-image");
const reservationTicketQrFallback = document.querySelector("#reservation-ticket-qr-fallback");

const state = {
  user: null,
  tickets: [],
};

function toTitleCase(value) {
  if (!value) {
    return "";
  }
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function ticketStatusLabel(status) {
  if (status === "checked_in") {
    return "Checked in";
  }
  if (status === "cancelled") {
    return "Cancelled";
  }
  return "Confirmed";
}

function buildTicketQrUrl(payload) {
  return `https://api.qrserver.com/v1/create-qr-code/?size=224x224&data=${encodeURIComponent(payload)}`;
}

function buildCountdownState(startAt) {
  const startDate = new Date(startAt || "");
  if (Number.isNaN(startDate.getTime())) {
    return { label: "Starts in 0d0h0m", isUrgent: false };
  }

  const diffMs = Math.max(startDate.getTime() - Date.now(), 0);
  const totalMinutes = Math.floor(diffMs / 60000);
  const days = Math.floor(totalMinutes / (60 * 24));
  const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
  const minutes = totalMinutes % 60;

  return {
    label: `Starts in ${days}d${hours}h${minutes}m`,
    isUrgent: diffMs > 0 && diffMs <= 86400000,
  };
}

function syncModalLock() {
  const hasOpenModal = Boolean(document.querySelector(".admin-modal:not(.hidden)"));
  document.body.classList.toggle("modal-open", hasOpenModal);
}

function openTicketModal(ticket) {
  if (!(reservationTicketModal instanceof HTMLElement) || !ticket) {
    return;
  }

  const quantity = Number(ticket.quantity || 1);
  const unitPrice = Number(ticket.ticket_price || 0);
  const totalPrice = Number(ticket.total_price || unitPrice * quantity || 0);
  const summaryParts = [
    `${quantity} ticket${quantity > 1 ? "s" : ""}`,
    formatCurrency(totalPrice),
    formatDateTime(ticket.start_at),
  ].filter(Boolean);

  if (reservationTicketTitle) {
    reservationTicketTitle.textContent = ticket.title || "Reservation ticket";
  }
  if (reservationTicketCode) {
    reservationTicketCode.textContent = ticket.ticket_code || "TICKET";
  }
  if (reservationTicketStatus) {
    reservationTicketStatus.textContent = ticketStatusLabel(ticket.status);
  }
  if (reservationTicketSummary) {
    reservationTicketSummary.textContent = summaryParts.join(" / ");
  }
  if (reservationTicketQrImage instanceof HTMLImageElement && reservationTicketQrFallback instanceof HTMLElement) {
    const qrPayload = String(ticket.qr_payload || "").trim();
    if (qrPayload) {
      reservationTicketQrImage.src = buildTicketQrUrl(qrPayload);
      reservationTicketQrImage.alt = `QR code for ${ticket.ticket_code || "ticket"}`;
      reservationTicketQrImage.classList.remove("hidden");
      reservationTicketQrFallback.classList.add("hidden");
    } else {
      reservationTicketQrImage.removeAttribute("src");
      reservationTicketQrImage.classList.add("hidden");
      reservationTicketQrFallback.classList.remove("hidden");
    }
  }
  if (reservationTicketMeta) {
    reservationTicketMeta.innerHTML = `
      <div>
        <dt>Ticket label</dt>
        <dd>${escapeHtml(ticket.ticket_label || "General Admission")}</dd>
      </div>
      <div>
        <dt>Quantity</dt>
        <dd>${escapeHtml(String(quantity))} ticket${quantity > 1 ? "s" : ""}</dd>
      </div>
      <div>
        <dt>Price per ticket</dt>
        <dd>${escapeHtml(formatCurrency(unitPrice))}</dd>
      </div>
      <div>
        <dt>Total</dt>
        <dd>${escapeHtml(formatCurrency(totalPrice))}</dd>
      </div>
      <div>
        <dt>Event starts</dt>
        <dd>${escapeHtml(formatDateTime(ticket.start_at))}</dd>
      </div>
      <div>
        <dt>Location</dt>
        <dd>${escapeHtml(ticket.location || "To be announced")}</dd>
      </div>
    `;
  }

  reservationTicketModal.classList.remove("hidden");
  reservationTicketModal.setAttribute("aria-hidden", "false");
  syncModalLock();
}

function closeTicketModal() {
  if (!(reservationTicketModal instanceof HTMLElement)) {
    return;
  }
  reservationTicketModal.classList.add("hidden");
  reservationTicketModal.setAttribute("aria-hidden", "true");
  syncModalLock();
}

function renderReservationMetrics() {
  const activeReservations = state.tickets.filter((ticket) => ticket.status === "confirmed" || ticket.status === "checked_in");
  const reservedTickets = state.tickets.reduce((sum, ticket) => sum + Number(ticket.quantity || 0), 0);

  if (reservationJoinedCount) {
    reservationJoinedCount.textContent = String(state.tickets.length);
  }
  if (reservationActiveCount) {
    reservationActiveCount.textContent = String(activeReservations.length);
  }
  if (reservationTicketCount) {
    reservationTicketCount.textContent = String(reservedTickets);
  }
}

function renderReservationList() {
  if (!reservationList) {
    return;
  }

  reservationList.classList.remove("is-placeholder");

  if (!state.tickets.length) {
    reservationList.classList.add("is-placeholder");
    reservationList.innerHTML = `
      <article class="event-match-empty activity-empty-card">
        <strong>No reservations yet</strong>
        <p>Reserve an event from the dashboard and your event ticket code will appear here.</p>
      </article>
    `;
    return;
  }

  reservationList.innerHTML = state.tickets
    .map((ticket) => {
      const countdown = buildCountdownState(ticket.start_at);
      return `
        <article class="event-match-card activity-registration-card">
          <div class="event-match-copy activity-registration-copy">
            <div>
              <div class="activity-request-head">
                <strong>${escapeHtml(ticket.title)}</strong>
                <span class="image-order-chip">${escapeHtml(ticket.ticket_code || "TICKET")}</span>
              </div>
              <p class="event-match-time">${escapeHtml(formatDateTime(ticket.start_at))}</p>
            </div>
            <dl class="event-match-meta activity-registration-meta activity-registration-meta-compact">
              <div>
                <dt>Location</dt>
                <dd>${escapeHtml(ticket.location || "To be announced")}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>${escapeHtml(ticketStatusLabel(ticket.status))}</dd>
              </div>
              <div class="activity-countdown-card ${countdown.isUrgent ? "is-urgent" : ""}">
                <dt>Time Remains</dt>
                <dd>${escapeHtml(countdown.label)}</dd>
              </div>
            </dl>
          </div>
          <div class="event-match-actions activity-registration-actions reservation-action-stack">
            <button class="detail-link" type="button" data-reservation-ticket="${escapeHtml(String(ticket.event_id))}">View ticket detail</button>
            <a class="detail-link" href="/events/${ticket.event_id}/view">View event detail</a>
          </div>
        </article>
      `;
    })
    .join("");
}

function populateHeader(user) {
  renderUserAvatar(reservationAvatar, user, "profile-avatar-image");
  if (reservationTitle) {
    reservationTitle.textContent = `${user.name}'s reservations`;
  }
  if (reservationHeroCopy) {
    reservationHeroCopy.textContent = `${user.email} - keep your joined events and ticket codes in one place.`;
  }
  if (reservationWelcomeText) {
    reservationWelcomeText.textContent = `Welcome, ${user.name}`;
  }
  if (reservationRoleChip) {
    reservationRoleChip.textContent = toTitleCase(user.role);
  }
  reservationAdminTopbarNav?.classList.toggle("hidden", user.role !== "admin");
  setupAccountMenu(user);
  setupGlobalFooter(user);
}

async function loadReservations() {
  const tickets = await api("/api/me/registrations");
  state.tickets = Array.isArray(tickets) ? tickets : [];
  renderReservationMetrics();
  renderReservationList();
}

function setupReservationInteractions() {
  reservationList?.addEventListener("click", (event) => {
    const target = event.target instanceof HTMLElement ? event.target.closest("[data-reservation-ticket]") : null;
    if (!(target instanceof HTMLElement)) {
      return;
    }

    const eventId = target.dataset.reservationTicket;
    const ticket = state.tickets.find((item) => String(item.event_id) === String(eventId));
    if (!ticket) {
      return;
    }

    openTicketModal(ticket);
  });

  reservationTicketModal?.addEventListener("click", (event) => {
    const target = event.target instanceof HTMLElement ? event.target.closest("[data-reservation-ticket-action='close']") : null;
    if (target) {
      closeTicketModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && reservationTicketModal instanceof HTMLElement && !reservationTicketModal.classList.contains("hidden")) {
      closeTicketModal();
    }
  });
}

async function boot() {
  const user = await getCurrentUser();
  if (!user) {
    redirectTo("/");
    return;
  }

  state.user = user;
  populateHeader(user);
  setupReservationInteractions();
  await loadReservations();
}

boot();
