from sqlmodel import Session, select
from database import engine, MarketplaceService

def seed_inventory():
    """
    Seeds the MarketplaceService table with inventory for DaPros
    """
    services = [
        {
            "service_name": "Comprehensive SEO Audit & Strategy",
            "category": "SEO",
            "estimated_cost": 299.00,
            "description": "In-depth technical, speed and on-page SEO audit for dapros.com.mx standards.",
            "provider_name": "DaPros Marketing",
            "is_active": True,
            "tenant_id": 1,
        },
        {
            "service_name": "Local SEO & Google Business Profile",
            "category": "SEO",
            "estimated_cost": 499.00,
            "description": "Google My Business setup, local citation building and Google Maps ranking.",
            "provider_name": "DaPros Marketing",
            "is_active": True,
            "tenant_id": 1,
        },
        {
            "service_name": "Desarrollo Web Next.js & React",
            "category": "Development",
            "estimated_cost": 1999.00,
            "description": "Custom modern high-converting web application and landing page development.",
            "provider_name": "DaPros Engineering",
            "is_active": True,
            "tenant_id": 1,
        },
        {
            "service_name": "Gestión de Campañas Google & Meta Ads",
            "category": "Marketing",
            "estimated_cost": 799.00,
            "description": "High ROI paid traffic management across Google Ads, Instagram and Facebook.",
            "provider_name": "DaPros Ads Team",
            "is_active": True,
            "tenant_id": 1,
        },
        {
            "service_name": "Diseño Gráfico & Identidad Visual",
            "category": "Design",
            "estimated_cost": 599.00,
            "description": "Full brand identity: logos, brand manuals, and digital advertising collateral.",
            "provider_name": "DaPros Creative",
            "is_active": True,
            "tenant_id": 1,
        },
        {
            "service_name": "Automatización con IA & Chatbots",
            "category": "AI Automation",
            "estimated_cost": 899.00,
            "description": "Intelligent AI assistant integration and CRM workflow automation for businesses.",
            "provider_name": "DaPros AI Lab",
            "is_active": True,
            "tenant_id": 1,
        }
    ]

    with Session(engine) as session:
        for s_data in services:
            existing = session.exec(
                select(MarketplaceService).where(MarketplaceService.service_name == s_data["service_name"])
            ).first()
            if not existing:
                service = MarketplaceService(**s_data)
                session.add(service)
        session.commit()
        print("Successfully seeded marketplace inventory for DaPros.")

if __name__ == "__main__":
    seed_inventory()
