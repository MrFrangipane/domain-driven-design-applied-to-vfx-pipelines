# Browser

`browser` is the third concrete example in this repository.

## Folder structure

```plain text
browser/
  application/
    __init__.py
    load_browser_items.py
    filter_browser_items.py

  browsing/
    __init__.py
    entities.py
    ports.py

  scanning/
    __init__.py
    filesystem.py
    ports.py

  presentation/
    __init__.py

    models/
      __init__.py
      browser_table_model.py
      browser_tree_model.py

    views/
      __init__.py
      main_window.py
      browser_view.py

    controllers/
      __init__.py
      browser_controller.py

  qt_app/
    __init__.py
    main.py

  __init__.py
```

## Core idea

## Running the example

## Package responsibilities

```plain text
application/
  Application use cases.

  This layer coordinates the browser workflow:
  loading files, parsing them, converting them into browser items,
  and applying filters.

browsing/
  Core browser concepts.

  This contains domain/application-facing objects such as browser items,
  browser filters, selected items, and repository-style ports.

scanning/
  File discovery interfaces and filesystem implementation.

  This is infrastructure-like because it talks to the real filesystem.

presentation/
  PySide6-facing presentation code.

  This contains Qt models, views, and controllers. It translates application
  results into things the GUI can display.

presentation/models/
  Qt item models.

  These classes adapt browser data into QAbstractTableModel,
  QAbstractItemModel, or similar PySide6 model classes.

presentation/views/
  Windows and widgets.

  These files define the visual interface: main window, browser panels,
  filters, buttons, menus, and selection widgets.

presentation/controllers/
  GUI coordination code.

  Controllers respond to button clicks, view events, and selection changes.
  They call application use cases and update Qt models/views.

qt_app/
  PySide6 application entry point and dependency wiring.

  This is where QApplication is created and where concrete implementations
  are connected together.
```

## More on Domain Driven Design

For further information about the Domain Driven Design approach used in this project, see:
