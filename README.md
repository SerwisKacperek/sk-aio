# SerwisKacperek-AllInOne (SK_AIO)

SK_AIO is a Python-based automation tool and plugin library designed to make it easy to add, develop, and manage plugins for automating a wide variety of tasks. The project provides a robust interface for plugin development, a modern TUI (Textual User Interface), and a flexible event-driven architecture.

## Features

- **Plugin-Based Architecture:** Easily extend the tool by developing new plugins to automate your workflows.
- **Modern TUI:** Built with [Textual](https://github.com/Textualize/textual) for a rich, interactive terminal experience.
- **Event-Driven:** Uses an event bus for communication between plugins and the core application.
- **Easy Plugin Development:** Well-defined APIs and base classes to help you create new plugins quickly.
- **Logging & Output:** Integrated logging and output areas for monitoring plugin actions and results.

## Getting Started

### Prerequisites
- Python 3.12.5 or newer

### Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/SerwisKacperek/sk-aio.git
cd sk_aio
pip install -r requirements.txt
```
> [!NOTE]  
> All plugin dependencies are managed and installed automatically by SK-AIO within the application itself. You do not need to install plugin dependencies manually.

### Running the application
To run the application normally, use:
```bash
python -m sk_aio
```

To run the application in development mode use:
```bash
textual console
```

Then run the app in another window using:
```bash
textual run -c sk_aio --dev
```

## Contributing
This application is currently in active development, and many aspects are subject to change.