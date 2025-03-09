import ImageCard from "../components/ImageCard";
import NavBar from "../components/NavBar";
import { useEffect, useState } from "react";

interface Movie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
}

export default function Watchlist() {
  const [movies, setMovies] = useState<Movie[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/movies/?preference=watch_later", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`, // Adjust based on auth
      },
    })
      .then((res) => res.json())
      .then((data) => setMovies(data))
      .catch((err) => console.error("Error fetching watchlist movies:", err));
  }, []);

  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-2xl font-bold text-white mb-4">
          Watch Later Movies
        </h1>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {movies.map((movie) => (
            <div key={movie.id}>
              <ImageCard
                imageUrl={`https://image.tmdb.org/t/p/original${movie.poster_path}`}
                title={movie.title}
                altText="A portrait-oriented image with 27:40 aspect ratio"
              ></ImageCard>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
