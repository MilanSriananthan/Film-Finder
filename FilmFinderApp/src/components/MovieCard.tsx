import { useState } from "react";
import ImageCard from "./ImageCard";
import InfoCard from "./InfoCard";
import { Movie } from "../types/Movie";
import { Info } from "lucide-react"; // Info icon

interface MovieCardProps {
  movie: Movie;
}

export default function MovieCard({ movie }: MovieCardProps) {
  const [showInfo, setShowInfo] = useState(false);

  return (
    <div className="relative">
      {/* Toggle between ImageCard and InfoCard */}
      {!showInfo ? (
        <ImageCard
          imageUrl={`https://image.tmdb.org/t/p/original${movie?.poster_path}`}
          title={movie?.title}
          altText={`Poster of ${movie?.title}`}
        />
      ) : (
        <InfoCard movie={movie} />
      )}

      {/* Info button stays visible in both views */}
      <button
        onClick={() => setShowInfo((prev) => !prev)}
        className="absolute top-2 right-2 bg-gray-900 text-white p-2 rounded-full hover:bg-gray-700"
      >
        <Info size={20} />
      </button>
    </div>
  );
}
