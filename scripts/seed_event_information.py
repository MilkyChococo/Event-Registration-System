from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from pymongo import ASCENDING, MongoClient, ReturnDocument

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import Settings
from app.services import DEFAULT_EVENT_IMAGE, build_location_map_url, utc_now


CONTACT_EMAIL = "thienphu210505@gmail.com"
CONTACT_PHONE = "0365349036"


EVENTS: list[dict[str, Any]] = [
    {
        "title": "TechFest 2026: Artificial Intelligence Breakthroughs",
        "description": "A premier gathering for tech enthusiasts, developers, and researchers to explore the latest advancements in GenAI, Machine Learning, and neural networks.",
        "category": "Tech Conference",
        "event_format": "Offline",
        "location": "Saigon Exhibition and Convention Center (SECC), District 7",
        "venue_details": "Saigon Exhibition and Convention Center (SECC), District 7.",
        "start_at": "2026-07-20T08:00:00",
        "registration_deadline": "2026-07-15T23:59:00",
        "capacity": 300,
        "registered_count": 180,
        "price": 35,
        "speaker_lineup": [
            "Dr. Hoang Nguyen - Head of AI Research, TechCore",
            "Sarah Jenkins - Lead Data Scientist, GlobalAI Solutions",
        ],
        "ticket_types": [
            {"label": "Standard Pass", "price": 35, "details": "Full access to keynotes and exhibition area."},
            {"label": "VIP Pass", "price": 89, "details": "Includes exclusive networking lunch and speaker meet-and-greet."},
        ],
        "refund_policy": "Full refund available until 7 days prior to the event.",
        "check_in_policy": "Present your QR code at the main registration desk at least 30 minutes before the opening keynote.",
    },
    {
        "title": "CyberSecurity Hackathon: Securing the Digital Foundation",
        "description": "An intensive 48-hour coding marathon where teams will build innovative security solutions to protect enterprise digital assets against modern cyber threats.",
        "category": "Programming Competition",
        "event_format": "Offline",
        "location": "Innovation Lab, 23 Nguyen Dinh Chieu Street, District 3",
        "venue_details": "Innovation Lab, 23 Nguyen Dinh Chieu Street, District 3.",
        "start_at": "2026-08-10T07:00:00",
        "registration_deadline": "2026-08-01T17:00:00",
        "capacity": 50,
        "registered_count": 35,
        "price": 15,
        "speaker_lineup": [
            "Tuan Le - Chief Security Officer, SecureNet",
            "Emily Tran - Cloud Security Architect, CyberFort",
        ],
        "ticket_types": [
            {"label": "Competitor Pass", "price": 15, "details": "Registration fee for one team member including meals."},
            {"label": "Observer Pass", "price": 5, "details": "Access to final pitch day and closing ceremony."},
        ],
        "refund_policy": "Non-refundable after registration deadline.",
        "check_in_policy": "Bring a valid ID and laptop. Check-in opens strictly at 6:30 AM.",
    },
    {
        "title": "DevOps Day: Enterprise System Optimization",
        "description": "Deep-dive sessions into CI/CD pipelines, containerization, and infrastructure as code to help engineering teams streamline their deployment processes.",
        "category": "Specialized Workshop",
        "event_format": "Offline",
        "location": "The Hive, 94 Xuan Thuy, Thao Dien, District 2",
        "venue_details": "The Hive, 94 Xuan Thuy, Thao Dien, District 2.",
        "start_at": "2026-09-12T09:00:00",
        "registration_deadline": "2026-09-05T12:00:00",
        "capacity": 100,
        "registered_count": 60,
        "price": 25,
        "speaker_lineup": [
            "David Smith - Senior DevOps Engineer, CloudScale",
            "Mai Pham - Site Reliability Expert, TechOps VN",
        ],
        "ticket_types": [
            {"label": "Standard Admission", "price": 25, "details": "Workshop access and digital materials."},
            {"label": "Premium Admission", "price": 65, "details": "Includes a 1-on-1 infrastructure consultation."},
        ],
        "refund_policy": "50% refund if canceled 3 days before the event.",
        "check_in_policy": "Display your booking confirmation email upon entry.",
    },
    {
        "title": "UIT Career Fair: Employer Connection 2026",
        "description": "Connect directly with top tech companies, submit your CV, and participate in on-the-spot interviews for internship and fresher roles.",
        "category": "Job Fair",
        "event_format": "Offline",
        "location": "Main Campus Courtyard, Linh Trung Ward, Thu Duc City",
        "venue_details": "Main Campus Courtyard, Linh Trung Ward, Thu Duc City.",
        "start_at": "2026-10-20T08:00:00",
        "registration_deadline": "2026-10-15T23:59:00",
        "capacity": 1000,
        "registered_count": 550,
        "price": 0,
        "speaker_lineup": ["HR Representatives from VNG, FPT Software, and Shopee"],
        "ticket_types": [
            {"label": "Student Pass", "price": 0, "details": "Free entry for all university students."},
            {"label": "Alumni Pass", "price": 0, "details": "Fast-track entry for graduated students."},
        ],
        "refund_policy": "Not applicable (Free event).",
        "check_in_policy": "Present your student ID card or alumni email confirmation at the gate.",
    },
    {
        "title": "Workshop: Conquering Global Study Abroad Scholarships",
        "description": "Learn the secrets to crafting a winning statement of purpose, securing strong recommendation letters, and acing scholarship interviews from successful alumni.",
        "category": "Skill Development Seminar",
        "event_format": "Offline",
        "location": "Liberty Central Hotel, 17 Ton Duc Thang, District 1",
        "venue_details": "Liberty Central Hotel, 17 Ton Duc Thang, District 1.",
        "start_at": "2026-11-05T14:00:00",
        "registration_deadline": "2026-11-02T10:00:00",
        "capacity": 80,
        "registered_count": 55,
        "price": 10,
        "speaker_lineup": [
            "Prof. Anh Vu - Academic Advisor, Global Edu",
            "Linh Hoang - Chevening Scholarship Alumnus",
        ],
        "ticket_types": [
            {"label": "General Entry", "price": 10, "details": "Seminar access and Q&A session."},
            {"label": "Mentorship Bundle", "price": 40, "details": "Includes a personal essay review session."},
        ],
        "refund_policy": "Full refund if requested 24 hours prior to the event.",
        "check_in_policy": "Show your e-ticket at the conference room entrance.",
    },
    {
        "title": "Youth Science Conference: Computer Vision Applications",
        "description": "A platform for young researchers to present their latest findings in object detection, semantic segmentation, and AI-driven image processing.",
        "category": "Academic Conference",
        "event_format": "Offline",
        "location": "Hall A, National University Ho Chi Minh City, Thu Duc City",
        "venue_details": "Hall A, National University Ho Chi Minh City, Thu Duc City.",
        "start_at": "2026-11-25T08:30:00",
        "registration_deadline": "2026-11-20T18:00:00",
        "capacity": 150,
        "registered_count": 90,
        "price": 20,
        "speaker_lineup": [
            "Dr. Binh Tran - Computer Vision Researcher",
            "Hung Le - AI Research Assistant",
        ],
        "ticket_types": [
            {"label": "Attendee Pass", "price": 20, "details": "Access to all paper presentations."},
            {"label": "Author Pass", "price": 50, "details": "Required for paper presenters, includes publication fee."},
        ],
        "refund_policy": "No refunds for Author Passes. Attendee Passes refundable up to 48 hours before.",
        "check_in_policy": "Pick up your badge at the registration desk using your confirmation code.",
    },
    {
        "title": "Summer Melodies: Viet Indie Music Night",
        "description": "A cozy music night featuring the best underground and indie artists in the city, performing acoustic sets and original summer tracks.",
        "category": "Live Concert",
        "event_format": "Offline",
        "location": "Acoustic Bar, 6E1 Ngo Thoi Nhiem, District 3",
        "venue_details": "Acoustic Bar, 6E1 Ngo Thoi Nhiem, District 3.",
        "start_at": "2026-12-01T20:00:00",
        "registration_deadline": "2026-12-01T12:00:00",
        "capacity": 200,
        "registered_count": 170,
        "price": 18,
        "speaker_lineup": ["Chillies (Guest Band)", "Vu (Headline Artist)"],
        "ticket_types": [
            {"label": "Standing Ticket", "price": 18, "details": "Floor access."},
            {"label": "VIP Seating", "price": 35, "details": "Reserved table with a complimentary drink."},
        ],
        "refund_policy": "All sales are final. Tickets are transferable.",
        "check_in_policy": "Doors open at 7:30 PM. Have your digital ticket ready to scan.",
    },
    {
        "title": "Art Exhibition: Colors of the Modern Metropolis",
        "description": "An immersive visual art experience showcasing paintings and digital artwork that reflect the chaos, beauty, and rapid growth of modern urban life.",
        "category": "Art & Culture",
        "event_format": "Offline",
        "location": "The Factory Contemporary Arts Centre, Thao Dien, District 2",
        "venue_details": "The Factory Contemporary Arts Centre, Thao Dien, District 2.",
        "start_at": "2026-12-15T10:00:00",
        "registration_deadline": "2026-12-10T17:00:00",
        "capacity": 250,
        "registered_count": 170,
        "price": 12,
        "speaker_lineup": [
            "Khoa Pham - Contemporary Artist",
            "Ly Nguyen - Art Curator",
        ],
        "ticket_types": [
            {"label": "Single Entry", "price": 12, "details": "One-time access to the gallery."},
            {"label": "Guided Tour Pass", "price": 25, "details": "Includes an audio guide and weekend curator walkthrough."},
        ],
        "refund_policy": "Tickets are valid for any day within the exhibition week; non-refundable.",
        "check_in_policy": "Walk-ins allowed. Present ticket at the front gate for wristband exchange.",
    },
    {
        "title": "UIT Marathon: Running for Community Health",
        "description": "A charity run to promote physical wellness and raise funds for local hospitals. Open to all students, professionals, and running enthusiasts.",
        "category": "Sports Event",
        "event_format": "Offline",
        "location": "Sala Park, Thu Thiem New Urban Area, District 2",
        "venue_details": "Sala Park, Thu Thiem New Urban Area, District 2.",
        "start_at": "2026-12-28T05:00:00",
        "registration_deadline": "2026-12-20T23:59:00",
        "capacity": 1000,
        "registered_count": 850,
        "price": 25,
        "speaker_lineup": ["Coach Tuan Anh - Marathon Specialist (Warm-up Session)"],
        "ticket_types": [
            {"label": "5KM Runner", "price": 25, "details": "Includes race bib and finisher medal."},
            {"label": "10KM Runner", "price": 35, "details": "Includes race bib, event T-shirt, and finisher medal."},
        ],
        "refund_policy": "No refunds. Participant kits will be mailed if unable to attend.",
        "check_in_policy": "Race kits must be collected two days prior to the event at the designated booth.",
    },
    {
        "title": "Volunteer Blood Donation Day: Sharing Drops of Red",
        "description": "Join hands to save lives in our bi-annual blood drive. Donors will receive a health check, certificate, and post-donation snacks.",
        "category": "Charity & Community",
        "event_format": "Offline",
        "location": "Student Cultural House, National University Village, Thu Duc City",
        "venue_details": "Student Cultural House, National University Village, Thu Duc City.",
        "start_at": "2027-01-08T07:30:00",
        "registration_deadline": "2027-01-05T08:00:00",
        "capacity": 300,
        "registered_count": 280,
        "price": 0,
        "speaker_lineup": ["Dr. Minh Chau - Hematology Department, Cho Ray Hospital"],
        "ticket_types": [
            {"label": "Blood Donor Registration", "price": 0, "details": "Reserve a time slot to donate."},
            {"label": "Volunteer Assistant", "price": 0, "details": "Register to help manage the event logistics."},
        ],
        "refund_policy": "Not applicable.",
        "check_in_policy": "Please bring a valid ID/CCCD. Ensure you have eaten breakfast and rested well before checking in.",
    },
]


def next_sequence(db: Any, sequence_name: str) -> int:
    document = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(document["value"])


def sync_event_counter(db: Any) -> None:
    highest = db.events.find_one({}, projection={"_id": 0, "id": 1}, sort=[("id", -1)])
    target = int(highest["id"]) if highest and "id" in highest else 0
    current = db.counters.find_one({"_id": "events"})
    current_value = int(current.get("value", 0)) if current else 0
    if target > current_value:
        db.counters.update_one({"_id": "events"}, {"$set": {"value": target}}, upsert=True)


def build_document(event_id: int, event_data: dict[str, Any], admin_id: int, timestamp: str) -> dict[str, Any]:
    location = event_data["location"]
    return {
        "id": event_id,
        **event_data,
        "organizer_name": "Event Registration System",
        "organizer_details": "Official event managed by Event Registration System.",
        "image_url": DEFAULT_EVENT_IMAGE,
        "image_urls": [DEFAULT_EVENT_IMAGE],
        "latitude": None,
        "longitude": None,
        "map_url": build_location_map_url(location),
        "contact_email": CONTACT_EMAIL,
        "contact_phone": CONTACT_PHONE,
        "opening_highlights": "Guest arrival, check-in, and opening session.",
        "mid_event_highlights": event_data["description"],
        "closing_highlights": "Closing remarks, networking, and participant wrap-up.",
        "created_by": admin_id,
        "approval_status": "approved",
        "review_note": "",
        "updated_at": timestamp,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Update MongoDB events from docs/event information.docx.")
    parser.add_argument("--prune-extra", action="store_true", help="Delete events beyond the 10 seeded records.")
    args = parser.parse_args()

    settings = Settings.from_env()
    client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    db = client[settings.mongo_db_name]

    db.users.create_index([("id", ASCENDING)], unique=True)
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.events.create_index([("id", ASCENDING)], unique=True)
    sync_event_counter(db)

    timestamp = utc_now()
    admin = db.users.find_one({"role": "admin"}, sort=[("id", ASCENDING)])
    if admin is None:
        admin_id = 1
    else:
        admin_id = int(admin["id"])

    existing_events = list(db.events.find({}, {"_id": 0, "id": 1}).sort("id", ASCENDING))
    existing_ids = [int(event["id"]) for event in existing_events]

    updated = 0
    inserted = 0
    seeded_ids: list[int] = []

    for index, event_data in enumerate(EVENTS):
        if index < len(existing_ids):
            event_id = existing_ids[index]
            existing = db.events.find_one({"id": event_id}) or {}
            document = build_document(event_id, event_data, admin_id, timestamp)
            document["created_at"] = existing.get("created_at") or timestamp
            db.events.update_one({"id": event_id}, {"$set": document}, upsert=True)
            updated += 1
        else:
            event_id = next_sequence(db, "events")
            document = build_document(event_id, event_data, admin_id, timestamp)
            document["created_at"] = timestamp
            db.events.insert_one(document)
            inserted += 1
        seeded_ids.append(event_id)

    deleted = 0
    if args.prune_extra:
        delete_result = db.events.delete_many({"id": {"$nin": seeded_ids}})
        db.registrations.delete_many({"event_id": {"$nin": seeded_ids}})
        deleted = int(delete_result.deleted_count)

    sync_event_counter(db)
    client.close()

    print(f"Updated {updated} event(s), inserted {inserted} event(s), deleted {deleted} extra event(s).")
    print(f"Seeded event IDs: {', '.join(str(event_id) for event_id in seeded_ids)}")


if __name__ == "__main__":
    main()
