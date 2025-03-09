import { useState } from "react";

export interface ImageCardProps {
  imageUrl: string;
  title: string;
  altText: string;
}

export default function ImageCard({
  imageUrl,
  title,
  altText,
}: ImageCardProps) {
  return (
    <div className="relative w-full overflow-hidden rounded-lg shadow-lg">
      <div className="aspect-[27/40]">
        <img
          src={imageUrl || "/placeholder.svg?height=400&width=270"}
          alt={altText}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <h2 className="text-white text-xl font-bold">{title}</h2>
        </div>
      </div>
    </div>
  );
}
