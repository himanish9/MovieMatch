'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

interface Movie {
  id: number;
  title: string;
  genre: string;
  rating: number;
  year: number;
  description: string;
  posterUrl?: string;
}

interface MovieCardProps {
  movie: Movie;
  rank: number;
}

export default function MovieCard({ movie, rank }: MovieCardProps) {
  const ratingColor =
    movie.rating >= 8.5
      ? 'text-accent'
      : movie.rating >= 7.5
        ? 'text-yellow-500'
        : 'text-orange-500';

  return (
    <Card className="group bg-card border-2 border-card hover:border-accent transition-all duration-300 overflow-hidden hover:shadow-lg hover:shadow-accent/20">
      <div className="relative overflow-hidden bg-secondary/50 aspect-video flex items-center justify-center">
        <div className="absolute top-3 left-3 bg-primary rounded-full w-10 h-10 flex items-center justify-center font-bold text-primary-foreground text-sm">
          #{rank}
        </div>
        <div className="text-6xl group-hover:scale-110 transition-transform duration-300">
          {movie.posterUrl || '🎬'}
        </div>
      </div>

      <div className="p-5 space-y-3">
        <div className="space-y-1">
          <h3 className="font-bold text-lg text-foreground group-hover:text-accent transition-colors">
            {movie.title}
          </h3>
          <div className="flex items-center justify-between">
            <p className="text-xs text-muted-foreground">{movie.genre}</p>
            <span className={`font-bold ${ratingColor}`}>{movie.rating}/10</span>
          </div>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2">
          {movie.description}
        </p>

        <div className="flex items-center justify-between pt-2 border-t border-border">
          <span className="text-xs text-muted-foreground">{movie.year}</span>
          <Link href={`/watch/${movie.id}`}>
            <Button
              size="sm"
              variant="ghost"
              className="h-8 text-accent hover:bg-accent/10 hover:text-accent text-xs"
            >
              Watch Now →
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
}
