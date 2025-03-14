import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import api from "../api";
import { Movie } from "../types/Movie";
import MovieGrid from "../components/MovieGrid";

export default function AllMovies() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [page, setPage] = useState(1); // Track current page
  const [hasMore, setHasMore] = useState(true); // Track if more movies exist

  useEffect(() => {
    api
      .get(`/api/movies/all/?page=${page}`)
      .then((response) => {
        if (response.data.results) {
          setMovies((prevMovies) => [...prevMovies, ...response.data.results]); // Append new movies
          setHasMore(response.data.next !== null); // Check if more pages exist
        }
      })
      .catch((err) => {
        console.error("Error fetching movies:", err);
      });
  }, [page]); // Re-run effect when `page` changes

  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-2xl font-bold text-black mb-4">All Movies</h1>
        <MovieGrid movies={movies} />

        {hasMore && (
          <button
            className="bg-blue-500 text-white p-2 rounded mt-4"
            onClick={() => setPage((prev) => prev + 1)}
          >
            Load More
          </button>
        )}
      </div>
    </>
  );
}
