# Film Finder

Film Finder is a movie recommendation web application that provides personalized movie suggestions based on user preferences. It utilizes collaborative filtering and machine learning to enhance recommendations, leveraging data from TMDB and MovieLens.

## Features

- **Movie Recommendations**: Personalized recommendations based on user interactions.
- **User Interactions**: Mark movies as liked, disliked, watch later, or not watched.
- **Avoids Repetitions**: Once a user interacts with a movie, it won’t appear again.
- **Hybrid Model**: Uses TMDB data and collaborative filtering for better suggestions.
- **Django Backend**: Manages API, authentication, and recommendation logic.
- **React Frontend**: Provides a seamless user experience.
- **PostgreSQL Database**: Stores user interactions and movie metadata.
- **Docker Support**: Containerized deployment for easy setup.

## Tech Stack

- **Frontend**: React
- **Backend**: Django (Django Rest Framework)
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Deployment**: Render

## Installation & Setup

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/film-finder.git
   cd film-finder/backend
   ```

2. Set up a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file and add:
   ```ini
   DATABASE_URL=your_postgres_database_url
   SECRET_KEY=your_django_secret_key
   TMDB_API_KEY=your_tmdb_api_key
   ```

5. Run migrations:
   ```sh
   python manage.py migrate
   ```

6. Start the backend server:
   ```sh
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```sh
   cd ../frontend
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the frontend server:
   ```sh
   npm run dev
   ```

## Deployment

The application is deployed on Render. Follow these steps:

1. Push your changes to GitHub.
2. Connect Render to your repository.
3. Set environment variables in Render’s dashboard.
4. Deploy the backend and frontend services.

## Environment Variables

Ensure the following environment variables are set:
```ini
DATABASE_URL=<your_postgres_db_url>
SECRET_KEY=<your_django_secret_key>
TMDB_API_KEY=<your_tmdb_api_key>
ALLOWED_HOSTS=film-finder-8twk.onrender.com
DEBUG=False
```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```sh
   git commit -m "Added new feature"
   ```
4. Push to GitHub and open a Pull Request.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

## Contact

For any issues or suggestions, feel free to reach out or create an issue on GitHub.

Happy Coding! 🎬🍿

