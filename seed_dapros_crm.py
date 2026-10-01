import os
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from sqlalchemy import text
from database import (
    engine, ClientProfile, Lead, Deal, Invoice, CRMQuote,
    ActivityLog, SentEmail, CallLog, Project, User
)

def seed_dapros_data():
    now = datetime.now(timezone.utc)
    print("Connecting to database and seeding DaPros CRM data...")

    with Session(engine) as session:
        # 1. Ensure all ClientProfiles have tenant_id = 1
        clients = session.exec(select(ClientProfile)).all()
        for c in clients:
            if c.tenant_id != 1:
                c.tenant_id = 1
                session.add(c)
        session.commit()
        print(f"Updated {len(clients)} client profiles with tenant_id=1.")

        # Find or use first client ID
        client_map = {c.companyName: c.id for c in clients}
        first_client_id = clients[0].id if clients else None

        # 2. Seed Leads for DaPros
        leads_data = [
            {
                "company_name": "Restaurante El Almacén GDL",
                "website": "https://elalmacengdl.com",
                "industry": "Restaurantes & Hospitalidad",
                "email": "contacto@elalmacengdl.com",
                "phone": "+52 33 1234 5678",
                "address": "Av. México 2890, Guadalajara, Jal.",
                "source": "Google Maps Radar",
                "status": "Positive",
                "notes": "Interested in online table booking system, QR menus, and local SEO ranking in Guadalajara.",
                "is_converted": False,
                "tenant_id": 1,
            },
            {
                "company_name": "Inmobiliaria Providencia",
                "website": "https://inmoprovidencia.mx",
                "industry": "Bienes Raíces",
                "email": "ventas@inmoprovidencia.mx",
                "phone": "+52 33 9876 5432",
                "address": "Av. Providencia 1450, Guadalajara, Jal.",
                "source": "Referral",
                "status": "New Lead",
                "notes": "Looking to redesign luxury property landing pages and run Meta/Google Ads for developments.",
                "is_converted": False,
                "tenant_id": 1,
            },
            {
                "company_name": "Logística Transmex",
                "website": "https://transmexlog.com",
                "industry": "Logística y Transporte",
                "email": "operaciones@transmexlog.com",
                "phone": "+52 33 5555 1212",
                "address": "Parque Industrial San Jorge, Zapopan, Jal.",
                "source": "Outbound Email",
                "status": "Converted",
                "notes": "Converted! Contract signed for modern tracking portal and corporate web development.",
                "is_converted": True,
                "tenant_id": 1,
            },
            {
                "company_name": "Clínica Dental Chapultepec",
                "website": "https://dentalchapultepec.com",
                "industry": "Salud y Bienestar",
                "email": "citas@dentalchapultepec.com",
                "phone": "+52 33 4444 8899",
                "address": "Av. Chapultepec Sur 230, Guadalajara, Jal.",
                "source": "Website Scraper",
                "status": "Neutral",
                "notes": "Requested a quote for monthly local SEO and Instagram content management.",
                "is_converted": False,
                "tenant_id": 1,
            },
            {
                "company_name": "Boutique Mezcal Artesanal",
                "website": "https://mezcalartesanaljal.mx",
                "industry": "E-Commerce / Bebidas",
                "email": "hola@mezcalartesanaljal.mx",
                "phone": "+52 33 7777 3344",
                "address": "Tlaquepaque Centro, Jal.",
                "source": "AI Email Agent",
                "status": "Positive",
                "notes": "High fit score. Proposing Shopify/Next.js e-commerce store with international shipping.",
                "is_converted": False,
                "tenant_id": 1,
            },
            {
                "company_name": "AutoPartes del Bajío",
                "website": "https://autopartesbajio.com",
                "industry": "Automotriz",
                "email": "ventas@autopartesbajio.com",
                "phone": "+52 47 7123 4567",
                "address": "Blvd. López Mateos, León, Gto.",
                "source": "Google Maps Radar",
                "status": "New Lead",
                "notes": "Non-responsive site, needs catalog search feature and Google Business Profile optimization.",
                "is_converted": False,
                "tenant_id": 1,
            },
            {
                "company_name": "Café & Tostaduría La Americana",
                "website": "https://tostaduriaamericana.mx",
                "industry": "Alimentos & Bebidas",
                "email": "cafe@tostaduriaamericana.mx",
                "phone": "+52 33 2222 9900",
                "address": "Colonia Americana, Guadalajara, Jal.",
                "source": "Local Outreach",
                "status": "Converted",
                "notes": "Full branding, packaging identity, and subscription web store launched.",
                "is_converted": True,
                "tenant_id": 1,
            },
            {
                "company_name": "Bufete Jurídico González & Asoc.",
                "website": "https://gonzalezjuridico.mx",
                "industry": "Servicios Legales",
                "email": "contacto@gonzalezjuridico.mx",
                "phone": "+52 33 6666 4433",
                "address": "Puerta de Hierro, Zapopan, Jal.",
                "source": "Outbound",
                "status": "Neutral",
                "notes": "Reviewed audit report, scheduled follow-up call with Emmanuel Padilla for next Tuesday.",
                "is_converted": False,
                "tenant_id": 1,
            }
        ]

        lead_ids = []
        for l_data in leads_data:
            existing = session.exec(select(Lead).where(Lead.company_name == l_data["company_name"])).first()
            if not existing:
                lead = Lead(**l_data)
                session.add(lead)
                session.commit()
                session.refresh(lead)
                lead_ids.append(lead.id)
            else:
                lead_ids.append(existing.id)
        print(f"Ensured {len(leads_data)} DaPros leads in database.")

        # 3. Seed Deals in Pipeline
        deals_data = [
            {"title": "Rediseño Web & Portal - Logística Transmex", "value": 3500.0, "stage": "Closed Won", "client_id": first_client_id, "tenant_id": 1},
            {"title": "Branding & E-Commerce - La Americana", "value": 4200.0, "stage": "Closed Won", "client_id": first_client_id, "tenant_id": 1},
            {"title": "Tienda en Línea Next.js - Mezcal Artesanal", "value": 2800.0, "stage": "Negotiation", "client_id": first_client_id, "tenant_id": 1},
            {"title": "Landing Page & Campañas Ads - Inmoprovidencia", "value": 1500.0, "stage": "Discovery", "client_id": first_client_id, "tenant_id": 1},
            {"title": "Estrategia Local SEO & GMB - El Almacén", "value": 1200.0, "stage": "Demo", "client_id": first_client_id, "tenant_id": 1},
            {"title": "Gestión Contenidos & Redes - Dental Chapultepec", "value": 950.0, "stage": "Lead", "client_id": first_client_id, "tenant_id": 1},
        ]
        for d_data in deals_data:
            existing = session.exec(select(Deal).where(Deal.title == d_data["title"])).first()
            if not existing:
                deal = Deal(**d_data)
                session.add(deal)
        session.commit()
        print("Ensured pipeline deals in database.")

        # 4. Seed Invoices for Financial Revenue Overview
        invoices_data = [
            {
                "invoice_number": "DAP-2026-001",
                "client_id": first_client_id,
                "amount": 3017.24,
                "tax": 482.76,
                "total": 3500.00,
                "currency": "USD",
                "status": "Paid",
                "paid_at": now - timedelta(days=25),
                "created_at": now - timedelta(days=28),
                "notes": "Sitio Web Corporativo y Sistema de Rastreo Transmex",
                "tenant_id": 1,
            },
            {
                "invoice_number": "DAP-2026-002",
                "client_id": first_client_id,
                "amount": 3620.69,
                "tax": 579.31,
                "total": 4200.00,
                "currency": "USD",
                "status": "Paid",
                "paid_at": now - timedelta(days=12),
                "created_at": now - timedelta(days=15),
                "notes": "Diseño de Marca, Empaque y Tienda Online La Americana",
                "tenant_id": 1,
            },
            {
                "invoice_number": "DAP-2026-003",
                "client_id": first_client_id,
                "amount": 1293.10,
                "tax": 206.90,
                "total": 1500.00,
                "currency": "USD",
                "status": "Paid",
                "paid_at": now - timedelta(days=3),
                "created_at": now - timedelta(days=5),
                "notes": "Auditoría Técnica SEO y Optimización de Velocidad",
                "tenant_id": 1,
            },
            {
                "invoice_number": "DAP-2026-004",
                "client_id": first_client_id,
                "amount": 2413.79,
                "tax": 386.21,
                "total": 2800.00,
                "currency": "USD",
                "status": "Sent",
                "due_date": (now + timedelta(days=10)).strftime("%Y-%m-%d"),
                "created_at": now - timedelta(days=2),
                "notes": "Desarrollo E-Commerce Boutique Mezcal Artesanal",
                "tenant_id": 1,
            },
            {
                "invoice_number": "DAP-2026-005",
                "client_id": first_client_id,
                "amount": 1034.48,
                "tax": 165.52,
                "total": 1200.00,
                "currency": "USD",
                "status": "Draft",
                "created_at": now - timedelta(days=1),
                "notes": "Posicionamiento Local y Campaña Google Ads El Almacén",
                "tenant_id": 1,
            }
        ]
        for inv_data in invoices_data:
            existing = session.exec(select(Invoice).where(Invoice.invoice_number == inv_data["invoice_number"])).first()
            if not existing:
                inv = Invoice(**inv_data)
                session.add(inv)
        session.commit()
        print("Ensured revenue invoices in database.")

        # 5. Seed CRM Quotes
        quotes_data = [
            {"quote_number": "COT-2026-01", "title": "Desarrollo Tienda Online Mezcal", "grand_total": 2800.0, "status": "Accepted", "client_id": first_client_id, "tenant_id": 1},
            {"quote_number": "COT-2026-02", "title": "Estrategia SEO Local Guadalajara", "grand_total": 1200.0, "status": "Accepted", "client_id": first_client_id, "tenant_id": 1},
            {"quote_number": "COT-2026-03", "title": "Landing Pages Inmobiliaria", "grand_total": 1500.0, "status": "Sent", "client_id": first_client_id, "tenant_id": 1},
        ]
        for q_data in quotes_data:
            existing = session.exec(select(CRMQuote).where(CRMQuote.quote_number == q_data["quote_number"])).first()
            if not existing:
                q = CRMQuote(**q_data)
                session.add(q)
        session.commit()
        print("Ensured CRM quotes in database.")

        # 6. Seed Activity Logs over last 7 days (for Engagement chart & Recent Activities list)
        activities = [
            ("Email Outreach", "Email", "Sent personalized bilingual proposal to Restaurante El Almacén GDL", 0),
            ("Payment Received", "Website", "Invoice DAP-2026-003 ($1,500 USD) marked as Paid", 0),
            ("Meeting Held", "In-person", "Strategy meeting with Inmobiliaria Providencia at Chapultepec office", 1),
            ("Quote Sent", "Email", "Sent formal quotation COT-2026-03 to Inmobiliaria Providencia", 1),
            ("Call Logged", "Phone", "Discovery call with Dr. Chapultepec (+52 33 4444 8899)", 2),
            ("Contract Signed", "Website", "Logística Transmex approved Website Redesign agreement", 2),
            ("New Lead Added", "Website", "AutoPartes del Bajío discovered and added to CRM", 3),
            ("Payment Received", "Website", "Invoice DAP-2026-002 ($4,200 USD) paid via wire transfer", 3),
            ("Email Outreach", "Email", "AI Email Agent sent outreach draft to Boutique Mezcal Artesanal", 4),
            ("SEO Audit Generated", "Website", "Completed technical SEO audit for Restaurante El Almacén GDL", 5),
            ("Discovery Call", "Phone", "Call with director of Bufete Jurídico González (+52 33 6666 4433)", 6),
            ("Project Milestone Completed", "Website", "La Americana web design final review completed", 6),
        ]
        for action, method, content, days_ago in activities:
            existing = session.exec(select(ActivityLog).where(ActivityLog.content == content)).first()
            if not existing:
                act = ActivityLog(
                    action=action,
                    method=method,
                    content=content,
                    details=f"DaPros CRM Activity - Logged by Emmanuel Padilla",
                    createdAt=now - timedelta(days=days_ago, hours=2),
                    tenant_id=1,
                    userId=1,
                    clientId=first_client_id
                )
                session.add(act)
        session.commit()
        print("Ensured 7-day activity logs in database.")

        # 7. Seed Call Logs over last 7 days
        calls = [
            ("+52 33 1234 5678", "Discovery call with El Almacén manager about online booking", 180, 0),
            ("+52 33 9876 5432", "Follow-up on landing page specifications with Inmobiliaria Providencia", 240, 1),
            ("+52 33 4444 8899", "Initial intro call with Clínica Dental Chapultepec", 120, 2),
            ("+52 33 7777 3344", "Mezcal Artesanal requirements gathering call", 300, 4),
            ("+52 33 6666 4433", "Legal firm proposal presentation with Lic. González", 420, 6),
        ]
        for phone, summary, duration, days_ago in calls:
            existing = session.exec(select(CallLog).where(CallLog.summary == summary)).first()
            if not existing:
                cl = CallLog(
                    phone_number=phone,
                    summary=summary,
                    duration_seconds=duration,
                    assigned_to="Emmanuel Padilla",
                    createdAt=now - timedelta(days=days_ago, hours=4),
                    received_at=now - timedelta(days=days_ago, hours=4),
                    tenant_id=1,
                    client_id=first_client_id
                )
                session.add(cl)
        session.commit()
        print("Ensured 7-day call logs in database.")

        # 8. Seed SentEmails
        sent_emails_data = [
            ("contacto@elalmacengdl.com", "Ayudemos a Restaurante El Almacén a crecer con reservas online y SEO", "Restaurante El Almacén GDL", 0),
            ("ventas@inmoprovidencia.mx", "Propuesta de Rediseño Web y Estrategia Google Ads", "Inmobiliaria Providencia", 1),
            ("hola@mezcalartesanaljal.mx", "Tienda en Línea Shopify / Next.js para Mezcal Artesanal", "Boutique Mezcal Artesanal", 2),
            ("citas@dentalchapultepec.com", "Plan de Posicionamiento Web y Presencia Digital", "Clínica Dental Chapultepec", 3),
            ("contacto@gonzalezjuridico.mx", "Sitio Web Corporativo y Auditoría SEO DaPros", "Bufete Jurídico González", 5),
        ]
        for to_email, subject, comp_name, days_ago in sent_emails_data:
            existing = session.exec(select(SentEmail).where(SentEmail.subject == subject)).first()
            if not existing:
                se = SentEmail(
                    to_email=to_email,
                    subject=subject,
                    english_body=f"Hi {comp_name},\n\nWe noticed great potential in your online visibility. DaPros is a digital agency based in Guadalajara specializing in high-converting web development and SEO.\n\nBest regards,\nEmmanuel Padilla\nFounder, DaPros\ncontacto@dapros.com.mx | +52 33 3184 9546",
                    spanish_body=f"Hola {comp_name},\n\nVimos una gran oportunidad para impulsar su presencia en línea y captación de clientes. En DaPros desarrollamos sitios web a la medida y estrategias SEO en Guadalajara.\n\nSaludos cordiales,\nEmmanuel Padilla\nFundador, DaPros\ncontacto@dapros.com.mx | +52 33 3184 9546",
                    sent_at=now - timedelta(days=days_ago, hours=1),
                    tenant_id=1,
                    status="Sent"
                )
                session.add(se)
        session.commit()
        print("Ensured sent emails in database.")

        # 9. Seed Projects
        projects_data = [
            {"name": "Rediseño Web Corporativo Transmex", "status": "In Progress", "progress": 65, "tenant_id": 1},
            {"name": "E-Commerce Mezcal Artesanal Jalisco", "status": "Planning", "progress": 30, "tenant_id": 1},
            {"name": "Sitio Web y Branding La Americana", "status": "Completed", "progress": 100, "tenant_id": 1},
            {"name": "Campaña SEO Clínica Dental Chapultepec", "status": "In Progress", "progress": 50, "tenant_id": 1},
        ]
        for p_data in projects_data:
            existing = session.exec(select(Project).where(Project.name == p_data["name"])).first()
            if not existing:
                proj = Project(**p_data)
                session.add(proj)
        session.commit()
        print("Ensured projects in database.")

    print("\nAll DaPros CRM data seeded successfully!")

if __name__ == "__main__":
    seed_dapros_data()
