import { useState } from "react";
import ImageCard from "./ImageCard";
import InfoCard from "./InfoCard";
import { Movie } from "../types/Movie";
import { Info, Download } from "lucide-react";
import api from "../api";

interface MovieCardProps {
  movie: Movie;
}

export default function MovieCard({ movie }: MovieCardProps) {
  const [showInfo, setShowInfo] = useState(false);
  const [clicked, setClicked] = useState(false);
  const handleDownload = async () => {
    try {
      await api.post("/api/add-movie/", {
        tmdbId: movie.tmdb_id,
      });
      setClicked(true);
    } catch (error) {
      console.error("Error sending movie to Radarr:", error);
    }
  };

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
      <button
        onClick={handleDownload}
        className={`absolute top-2 left-2 p-2 rounded-full 
          ${clicked ? "bg-green-500" : "bg-gray-900"} 
          text-white hover:bg-gray-700`}
      >
        <Download size={20} />
      </button>
      <button
        onClick={() => setShowInfo((prev) => !prev)}
        className="absolute top-2 right-2 bg-gray-900 text-white p-2 rounded-full hover:bg-gray-700"
      >
        <Info size={20} id="info_button" />
      </button>
    </div>
  );
}
