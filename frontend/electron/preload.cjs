const {
    contextBridge,
    ipcRenderer
} = require("electron");

contextBridge.exposeInMainWorld(

    "electronAPI",

    {
        hideWindow: () => {

            ipcRenderer.send(
                "hide-window"
            );
        }
    }
);