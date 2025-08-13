# monitoring/metrics_collector.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import psutil

# Define metrics
REQUEST_COUNT = Counter('trade_api_requests_total', 'Total API requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('trade_api_request_duration_seconds', 'Request latency')
MODEL_PREDICTIONS = Counter('ml_model_predictions_total', 'Total ML predictions', ['model_type'])
ACTIVE_USERS = Gauge('trade_dashboard_active_users', 'Number of active dashboard users')

# Add system metrics
SYSTEM_CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
SYSTEM_MEMORY_USAGE = Gauge('system_memory_usage_percent', 'Memory usage percentage')

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
    
    def track_api_request(self, method: str, endpoint: str, duration: float):
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_LATENCY.observe(duration)
    
    def track_model_prediction(self, model_type: str):
        MODEL_PREDICTIONS.labels(model_type=model_type).inc()
    
    def update_system_metrics(self):
        """Update system performance metrics"""
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        
        # Update Prometheus metrics
        SYSTEM_CPU_USAGE.set(cpu_usage)
        SYSTEM_MEMORY_USAGE.set(memory_usage)
    
    def start_metrics_server(self, port: int = 8000):
        """Start the Prometheus metrics HTTP server"""
        start_http_server(port)
        print(f"Metrics server started on port {port}")
