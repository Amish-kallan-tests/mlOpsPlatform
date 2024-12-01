from app import create_app
from app.scheduler import schedule_deployments
import threading

app = create_app()

if __name__ == '__main__':
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_deployments)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
