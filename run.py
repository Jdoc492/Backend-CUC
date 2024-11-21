from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Para desarrollo local
    with app.app_context():
        db.create_all()

    print("Servidor Flask corriendo en http://127.0.0.1:5000")
    app.run(debug=True)  # Mantén esto para desarrollo local
