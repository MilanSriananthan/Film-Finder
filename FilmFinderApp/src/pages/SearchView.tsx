import NavBar from "../components/NavBar";
import SearchBar from "../components/SearchBar";
import { useState } from "react";
import api from "../api";
import { Movie } from "../types/Movie";
import MovieGrid from "../components/MovieGrid";

export default function SearchView() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [externalMovies, setExternalMovies] = useState<Movie[]>([]);

  const externalSearch = (query: string) => {
    api
      .get(`/api/movies/search/`, {
        params: { query: query },
      })
      .then((response) => {
        if (response.data) {
          setExternalMovies(response.data);
          console.log(externalMovies);
        }
      })
      .catch((err) => {
        console.error("Error fetching movies:", err);
      });
  };

  const handleSearch = (query: string) => {
    externalSearch(query);
    api
      .get(`/api/movies/all/?title=${query}`)
      .then((response) => {
        if (response.data.results) {
          setMovies(response.data.results); // Directly set the movies response
          console.log(response.data.results); // Log the fetched results
        }
      })
      .catch((err) => {
        console.error("Error fetching movies:", err);
      });
  };

  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} />
        </div>
        {/* Render the movies */}
        <div className="mt-4">
          {movies.length + externalMovies.length > 0 ? (
            <MovieGrid movies={[...movies, ...externalMovies]} />
          ) : (
            <p className="text-center text-lg text-gray-500">No movies found</p>
          )}
        </div>
      </div>
    </>
  );
}
