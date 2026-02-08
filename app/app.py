from flask import Flask, request, jsonify, redirect
from app.models import db, URL
from app.utils import generate_short_code
from app.config import Config
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Health check endpoints
    @app.route('/health/live', methods=['GET'])
    def liveness():
        return jsonify({'status': 'alive'}), 200

    @app.route('/health/ready', methods=['GET'])
    def readiness():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'ready'}), 200
        except Exception as e:
            return jsonify({'status': 'not ready', 'error': str(e)}), 503

    # API endpoints
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        original_url = data['url']

        # Validación básica de URL
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400

        # Generar código único con retry para manejar race conditions
        max_retries = 5
        for attempt in range(max_retries):
            short_code = generate_short_code()
            try:
                url_entry = URL(original_url=original_url, short_code=short_code)
                db.session.add(url_entry)
                db.session.commit()
                return jsonify(url_entry.to_dict()), 201
            except IntegrityError:
                db.session.rollback()
                if attempt == max_retries - 1:
                    return jsonify({'error': 'Could not generate unique code, try again'}), 503

    @app.route('/<short_code>', methods=['GET'])
    def redirect_to_url(short_code):
        url_entry = URL.query.filter_by(short_code=short_code).first()

        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404

        # Comprobar si la URL ha expirado
        if url_entry.expires_at and url_entry.expires_at < datetime.utcnow():
            return jsonify({'error': 'URL has expired'}), 410

        # Incrementar contador de clicks
        url_entry.clicks += 1
        db.session.commit()

        return redirect(url_entry.original_url, code=302)

    @app.route('/stats/<short_code>', methods=['GET'])
    def get_stats(short_code):
        url_entry = URL.query.filter_by(short_code=short_code).first()

        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404

        return jsonify(url_entry.to_dict()), 200

    @app.route('/urls', methods=['GET'])
    def list_urls():
        urls = URL.query.order_by(URL.created_at.desc()).limit(100).all()
        return jsonify([url.to_dict() for url in urls]), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
