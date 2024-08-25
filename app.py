from nicegui import ui

def button_clicked():
    ui.notify('Button clicked!')

ui.button('Click me', on_click=button_clicked)

ui.run(host='0.0.0.0', port=7777)