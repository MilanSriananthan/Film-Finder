import { Movie } from "../types/Movie";
import MovieCard from "../components/MovieCard";

interface MovieCardProps {
  movies: Movie[];
}

export default function MovieGrid({ movies }: MovieCardProps) {
  return (
    <>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {movies.map((movie) => (
          <div key={movie.movie_id}>
            <MovieCard movie={movie}></MovieCard>
          </div>
        ))}
      </div>
    </>
  );
}
