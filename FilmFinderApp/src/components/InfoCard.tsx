import { motion } from "framer-motion";
import { Movie } from "../types/Movie";

interface InfoCardProps {
  movie: Movie;
}

export default function InfoCard({ movie }: InfoCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      transition={{ duration: 0.3 }}
      className="relative w-full max-w-sm overflow-hidden rounded-lg shadow-lg bg-gray-900 text-white p-4"
    >
      <div className="bg-white w-full shadow-lg overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            {movie.title}
          </h3>
        </div>
        <div className="border-t border-gray-200">
          <dl className="space-y-4 p-4">
            <div className="flex justify-between">
              <dt className="text-sm font-medium text-gray-500">Language</dt>
              <dd className="text-sm text-gray-900">
                {movie.original_language}
              </dd>
            </div>
            <div className="flex flex-col">
              <dt className="text-sm font-medium text-gray-500">Description</dt>
              <dd className="text-sm text-gray-900 break-words">
                {movie.overview}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm font-medium text-gray-500">
                Release Date
              </dt>
              <dd className="text-sm text-gray-900">{movie.release_date}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm font-medium text-gray-500">Popularity</dt>
              <dd className="text-sm text-gray-900">{movie.popularity}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm font-medium text-gray-500">Rating</dt>
              <dd className="text-sm text-gray-900">
                {movie.vote_average} ({movie.vote_count} votes)
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </motion.div>
  );
}
