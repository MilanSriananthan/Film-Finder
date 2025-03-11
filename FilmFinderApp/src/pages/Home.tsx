import ImageCard from "../components/ImageCard";
import ButtonRow from "../components/ButtonRow";
import NavBar from "../components/NavBar";
import { useState, useEffect, useRef } from "react";
import api from "../api";
import { Info } from "lucide-react";
import InfoCard from "../components/InfoCard";

interface Movie {
  adult: boolean;
  backdrop_path: string;
  genre_ids: number[];
  id: number;
  tmdb_id: number;
  original_language: string;
  original_title: string;
  overview: string;
  popularity: number;
  poster_path: string;
  release_date: string;
  title: string;
  video: boolean;
  vote_average: number;
  vote_count: number;
  preferences: string;
}

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [currentMovieIndex, setCurrentMovieIndex] = useState(0);
  const pageRef = useRef(1);
  const [page, setPage] = useState(() => pageRef.current);
  const [showInfo, setShowInfo] = useState(false);

  useEffect(() => {
    if (movies.length > 0) return;
    setCurrentMovieIndex(0);
    pageRef.current = page;
    const fetchMovies = async () => {
      try {
        pageRef.current = page;
        // Fetch top-rated movies
        const response = await api.get(`/api/movies-details/?page=${page}`);
        const data = response.data;
        const allMovies: Movie[] = data.movies;
        // Fetch saved movies from the database
        const savedMoviesResponse = await api.get("/api/movies/");
        const savedMovies: Movie[] = savedMoviesResponse.data;

        // Get IDs of saved movies
        const savedMovieIds = new Set(savedMovies.map((movie) => movie.id));

        // Filter out already saved movies
        const filteredMovies = allMovies.filter(
          (movie) => !savedMovieIds.has(movie.id)
        );

        if (filteredMovies.length === 0) {
          setTimeout(() => {
            setPage((prevPage) => prevPage + 1);
            setCurrentMovieIndex(0); // Delayed to prevent race conditions
          }, 100);
        } else {
          setMovies(filteredMovies);
          setCurrentMovieIndex(0);
        }
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    fetchMovies();
  }, [page, movies.length]);

  const nextMovie = () => {
    if (currentMovieIndex < movies.length - 1) {
      setCurrentMovieIndex(currentMovieIndex + 1);
    } else {
      console.log("🎯 End of movies reached, fetching next page...");
      setMovies([]); // Clear current movies
      setPage((prevPage) => prevPage + 1); // Increment page
    }
  };

  const saveMovieInteraction = (
    preferences: "liked" | "disliked" | "watch_later" | "not_watched"
  ) => {
    if (movies.length === 0) return;
    const movie = movies[currentMovieIndex];
    api
      .post("/api/movies/", {
        ...movie,
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
