from app import app, db, CategoryAllocation

with app.app_context():
    # Drop the old table (with weekly_allocation column)
    CategoryAllocation.__table__.drop(db.engine)
    print("🗑️ Dropped 'category_allocations' table.")

    # Recreate table based on updated model (without weekly_allocation)
    db.create_all()
    print("✅ Recreated table with updated schema.")
