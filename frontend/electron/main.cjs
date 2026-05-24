const {
    app,
    BrowserWindow,
    Tray,
    Menu,
    screen,
    ipcMain
} = require("electron");

const path = require("path");

let mainWindow;
let tray;

function createWindow() {

    const primaryDisplay =
        screen.getPrimaryDisplay();

    const {
        width,
        height
    } = primaryDisplay.workAreaSize;

    mainWindow = new BrowserWindow({

        width: 420,
        height: 700,

        x: width - 430,
        y: height - 720,

        frame: false,

        transparent: true,

        alwaysOnTop: true,

        resizable: false,

        skipTaskbar: true,

        show: false,

        hasShadow: true,

        webPreferences: {

            preload: path.join(
                __dirname,
                "preload.cjs"
            ),

            contextIsolation: true,

            nodeIntegration: false
        }
    });

    mainWindow.loadURL(
        "http://localhost:5173"
    );

    mainWindow.setVisibleOnAllWorkspaces(
        true,
        {
            visibleOnFullScreen: true
        }
    );

    mainWindow.on("blur", () => {

    });
}

function createTray() {

    tray = new Tray(

        path.join(
            __dirname,
            "icon.png"
        )
    );

    const contextMenu =
        Menu.buildFromTemplate([

            {
                label: "Open Friday",

                click: () => {

                    mainWindow.show();

                    mainWindow.focus();
                }
            },

            {
                label: "Hide Friday",

                click: () => {

                    mainWindow.hide();
                }
            },

            {
                type: "separator"
            },

            {
                label: "Exit",

                click: () => {

                    app.quit();
                }
            }
        ]);

    tray.setToolTip(
        "Friday Assistant"
    );

    tray.setContextMenu(
        contextMenu
    );

    tray.on("click", () => {

        if (mainWindow.isVisible()) {

            mainWindow.hide();

        } else {

            mainWindow.show();

            mainWindow.focus();
        }
    });
}

app.whenReady().then(() => {

    createWindow();

    createTray();

    ipcMain.on(

        "hide-window",

        () => {

            mainWindow.hide();
        }
    );

    app.on("activate", () => {

        if (
            BrowserWindow
                .getAllWindows()
                .length === 0
        ) {

            createWindow();
        }
    });
});

app.on(
    "window-all-closed",
    (e) => {

        e.preventDefault();
    }
);