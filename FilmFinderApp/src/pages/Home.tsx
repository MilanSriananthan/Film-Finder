import ImageCard from "../components/ImageCard";
import ButtonRow from "../components/ButtonRow";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import api from "../api";
import { Info } from "lucide-react";
import InfoCard from "../components/InfoCard";

interface Movie {
  movie_id: number;
  imdb_id: string;
  tmdb_id: number;
  title: string;
  adult: boolean;
  backdrop_path: string;
  genre_ids: number[];
  original_language: string;
  original_title: string;
  overview: string;
  popularity: number;
  poster_path: string;
  release_date: string;
  video: boolean;
  vote_average: number;
  vote_count: number;
  preferences: string;
}

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [currentMovieIndex, setCurrentMovieIndex] = useState(0);
  const [showInfo, setShowInfo] = useState(false);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        // Fetch top-rated movies
        const response = await api.get(`/api/movies-details/`);
        const data = response.data;
        const filteredMovies: Movie[] = data.movies;
        setMovies(filteredMovies);
        setCurrentMovieIndex(0);
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    fetchMovies();
  }, []);

  const nextMovie = () => {
    if (currentMovieIndex < movies.length - 1) {
      setCurrentMovieIndex(currentMovieIndex + 1);
    } else {
      console.log("🎯 End of movies reached, fetching next set...");
      setMovies([]);
    }
  };

  const saveMovieInteraction = (
    preferences: "liked" | "disliked" | "watch_later" | "not_watched"
  ) => {
    if (movies.length === 0) return;
    const movie: Movie = movies[currentMovieIndex];
    api
      .post("/api/movies/", {
        movie_details: movie.movie_id,
        preferences,
      })
      .then((res) => {
        if (res.status !== 201) alert("Failed to interact with movie.");
      })
      .catch((err) => alert(err));
    nextMovie();
  };

  return (
    <>
      <NavBar />
      <main className="flex min-h-screen flex-col items-center justify-center p-16 relative">
        {/* ImageCard Wrapper (Keeps ImageCard in place) */}
        <div className="relative w-full flex justify-center">
          {/* ImageCard */}
          <div className="max-w-md">
            <ImageCard
              imageUrl={`https://image.tmdb.org/t/p/original${movies[currentMovieIndex]?.poster_path}`}
              title={movies[currentMovieIndex]?.title}
              altText="A portrait-oriented image with 27:40 aspect ratio"
            />
          </div>

          {/* InfoCard (Absolutely Positioned to the Right) */}
          {showInfo && (
            <div className="absolute right-52 ml-8 w-full max-w-md">
              <InfoCard movie={movies[currentMovieIndex]} />
            </div>
          )}
        </div>

        {/* Buttons Row */}
        <div className="flex w-full max-w-lg justify-between mt-4">
          <ButtonRow interactionHandler={saveMovieInteraction} />
          {/* Info Button */}
          <button
            className="p-2 rounded-full bg-black/60 hover:bg-black/80 focus:outline-none focus:ring-2 focus:ring-white"
            aria-label="More info"
            onClick={() => setShowInfo(!showInfo)}
          >
            <Info className="text-white w-6 h-6" />
          </button>
        </div>
      </main>
    </>
  );
}
