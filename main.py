import asyncio
import logging

from auth.login import login, register, logout_all
from utils.menus import auth_menu, admin_menu, user_menu
from core.models import *
from services.products import *
from services.menu_products import *
from services.orders import *
from services.orders import close_expired_durations

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Application started")

    logout_all()

    return await auth_flow()

async def auth_flow() -> None:
    print(auth_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        role = await login()

        if role == "admin":
            return await admin_panel()

        if role == "user":
            return await user_panel()

        return await auth_flow()

    if choice == "2":
        if register():
            print("account successfully registered")
        return await auth_flow()

    logger.info("Application exit")
    return



async def after_login() -> None:
    user = get_active_user()

    if not user:
        return await auth_flow()

    if user["is_admin"]:
        logger.info("Admin panel auto-opened")
        return await admin_panel()

    logger.info("User panel auto-opened")
    return await user_panel()


async def admin_panel() -> None:
    print(admin_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        products = show_all_products()

        if not products:
            print("No products found")
        else:
            for p in products:
                print(f"{p['id']}. {p['title']} - {p['price']}")

        return await admin_panel()

    if choice == "2":
        add_product()
        return await admin_panel()

    if choice == "3":
        delete_product()
        return await admin_panel()

    if choice == "4":
        print(show_today_menu())
        return await admin_panel()

    if choice == "5":
        add_product_to_menu()
        return await admin_panel()

    if choice == "6":
        remove_product_from_menu()
        return await admin_panel()

    if choice == "7":
        orders = show_all_orders()

        if not orders:
            print("No orders")
        else:
            for o in orders:
                print(
                    f"{o['id']} | {o['username']} | {o['title']} | "
                    f"{o['amount']} | active={o['status']}"
                )

        return await admin_panel()


    if choice == "8":
        change_order_status()
        return await admin_panel()

    logger.info("Exit admin panel")
    return await auth_flow()

async def user_panel() -> None:
    close_expired_durations()

    print(user_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        menu = show_today_menu()

        if not menu:
            print("Today's menu is empty")
        else:
            for m in menu:
                print(f"{m['id']}. {m['title']} - {m['price']} ({m['amount']})")

        return await user_panel()

    if choice == "2":
        make_order()
        return await user_panel()

    if choice == "3":
        orders = show_my_orders()

        if not orders:
            print("You have no orders")
            return user_panel()

        for o in orders:
            order_type = "Dine in" if o["order_type"] else "Take away"
            status = "Active" if o["status"] else "Finished"

            print(
                f"{o['id']}. {o['title']} | {o['amount']} | "
                f"{order_type} | {status} | "
                f"{o['created_at']:%Y-%m-%d %H:%M}"
            )

        return await user_panel()


    if choice == "4":
        cancel_order()
        return await user_panel()

    logger.info("Exit user panel")
    return await auth_flow()


if __name__=="__main__":
    # execute_query(users)
    # execute_query(products)
    # execute_query(menu_products)
    # execute_query(orders)
    # execute_query(durations)

    asyncio.run(main())