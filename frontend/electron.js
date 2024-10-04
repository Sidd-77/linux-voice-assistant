import { app, BrowserWindow } from "electron";

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    fullscreen: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true, // Required if you're using Node.js features in the renderer
      enableRemoteModule: true,
      media: { audio: true, video: false }, // Enable microphone (audio)
    },
    frame: false, // Remove native window frame for a more app-like feel
  });

  win.loadURL('http://localhost:5173'); // Your React app
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
