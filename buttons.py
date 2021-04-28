
def build_menu(buttons, n_cols, header_buttons=None, header_buttons1=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
        menu.insert(1, header_buttons1)

    if footer_buttons:
        menu.append(footer_buttons)

    return menu