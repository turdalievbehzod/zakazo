import logging

from auth.login import login, register, logout_all
from utils.menus import auth_menu, admin_menu, user_menu

from services.products import *
from services.menu_products import *
from services.orders import *
from services.orders import close_expired_durations

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Application started")

    logout_all()

    return auth_flow()

def auth_flow() -> None:
    print(auth_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        if login():
            return after_login()
        return auth_flow()

    if choice == "2":
        register()
        return auth_flow()

    return


def after_login() -> None:
    user = get_active_user()

    if not user:
        return auth_flow()

    if user["is_admin"]:
        logger.info("Admin panel auto-opened")
        return admin_panel()

    logger.info("User panel auto-opened")
    return user_panel()


def admin_panel() -> None:
    print(admin_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        print(show_all_products())
        return admin_panel()

    if choice == "2":
        add_product()
        return admin_panel()

    if choice == "3":
        delete_product()
        return admin_panel()

    if choice == "4":
        print(show_today_menu())
        return admin_panel()

    if choice == "5":
        add_product_to_menu()
        return admin_panel()

    if choice == "6":
        remove_product_from_menu()
        return admin_panel()

    if choice == "7":
        print(show_all_orders())
        return admin_panel()

    if choice == "8":
        change_order_status()
        return admin_panel()

    logger.info("Exit admin panel")
    return auth_flow()

def user_panel() -> None:
    close_expired_durations()

    print(user_menu)
    choice: str = input("Choice: ")

    if choice == "1":
        print(show_today_menu())
        return user_panel()

    if choice == "2":
        make_order()
        return user_panel()

    if choice == "3":
        print(show_my_orders())
        return user_panel()

    if choice == "4":
        cancel_order()
        return user_panel()

    logger.info("Exit user panel")
    return auth_flow()

if __name__=="__main__":
    main()