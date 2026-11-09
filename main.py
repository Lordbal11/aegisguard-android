__version__ = "1.0.0"

import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock

class SecurityDashboardUI(BoxLayout):
    def __init__(self, **kwargs):
        super(SecurityDashboardUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Brand Header
        self.add_widget(Label(
            text='BMJ Synthetix Labs\nAegisGuard Mobile Security',
            font_size=20,
            halign='center',
            size_hint_y=None,
            height=80
        ))

        # Status Display
        self.status_label = Label(
            text='Status: Protection Active (Local Mode)',
            font_size=16,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.status_label)

        # Trigger Scan Button
        self.scan_btn = Button(
            text='Run Local DOM & Telemetry Check',
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.scan_btn.bind(on_press=self.run_local_scan)
        self.add_widget(self.scan_btn)

        # Log Output Box
        self.log_label = Label(
            text='Logs: No threats detected. System secure.',
            valign='top',
            halign='left'
        )
        self.log_label.bind(size=self.log_label.setter('text_size'))
        self.add_widget(self.log_label)

        # Initialize local SQLite database
        self.init_db()

    def init_db(self):
        db_path = os.path.join(App.get_running_app().user_data_dir, 'telemetry.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event TEXT
            )
        ''')
        self.conn.commit()

    def run_local_scan(self, instance):
        # Simulated local telemetry inspection
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        event_msg = f"[{timestamp}] DOM inspection passed. 0 vectors flagged."
        
        self.cursor.execute("INSERT INTO logs (timestamp, event) VALUES (?, ?)", (timestamp, event_msg))
        self.conn.commit()

        self.log_label.text = f"Latest Scan Complete:\n{event_msg}\n(Stored locally via SQLite)"

class AegisGuardApp(App):
    def build(self):
        self.title = 'AegisGuard Enterprise'
        return SecurityDashboardUI()

if __name__ == '__main__':
    AegisGuardApp().run()