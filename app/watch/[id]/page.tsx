'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface Movie {
  id: number;
  title: string;
  genre: string;
  rating: number;
  year: number;
  description: string;
  posterUrl?: string;
}

const allMovies: Movie[] = [
  // Horror Movies
  { id: 1, title: 'Kishkindhapuri', genre: 'Horror', rating: 6.9, year: 2025, description: 'Horror film', posterUrl: '👻' },
  { id: 2, title: 'Ghatikachalam', genre: 'Horror', rating: 6.1, year: 2025, description: 'Horror film', posterUrl: '👻' },
  { id: 3, title: 'Subham', genre: 'Horror', rating: 7.2, year: 2025, description: 'Horror film', posterUrl: '👻' },
  { id: 4, title: 'Jatadhara', genre: 'Horror', rating: 3.3, year: 2025, description: 'Horror film', posterUrl: '👻' },
  { id: 5, title: 'Odela 2', genre: 'Horror', rating: 4.6, year: 2025, description: 'Horror film', posterUrl: '👻' },
  { id: 6, title: 'Eesha', genre: 'Horror', rating: 9.1, year: 2024, description: 'Horror film', posterUrl: '👻' },
  { id: 7, title: 'Kalinga', genre: 'Horror', rating: 6.6, year: 2024, description: 'Horror film', posterUrl: '👻' },
  { id: 8, title: 'Demonte Colony 2', genre: 'Horror', rating: 6.5, year: 2024, description: 'Horror film', posterUrl: '👻' },
  { id: 9, title: 'Geethanjali Malli Vachindi', genre: 'Horror', rating: 4.7, year: 2024, description: 'Horror film', posterUrl: '👻' },
  { id: 10, title: 'Tantra', genre: 'Horror', rating: 4.9, year: 2024, description: 'Horror film', posterUrl: '👻' },
  
  // Comedy Movies
  { id: 11, title: 'Mathu Vadalara 2', genre: 'Comedy', rating: 8.2, year: 2024, description: 'Comedy film', posterUrl: '😂' },
  { id: 12, title: 'Aay', genre: 'Comedy', rating: 7.5, year: 2024, description: 'Comedy film', posterUrl: '😂' },
  { id: 13, title: 'Maruthi Nagar Subramanyam', genre: 'Comedy', rating: 7.2, year: 2024, description: 'Comedy film', posterUrl: '😂' },
  { id: 14, title: '35 Chinna Katha Kaadu', genre: 'Comedy', rating: 7.8, year: 2024, description: 'Comedy film', posterUrl: '😂' },
  { id: 15, title: 'MAD', genre: 'Comedy', rating: 7.3, year: 2023, description: 'Comedy film', posterUrl: '😂' },
  { id: 16, title: 'Janaka Aithe Ganaka', genre: 'Comedy', rating: 6.5, year: 2024, description: 'Comedy film', posterUrl: '😂' },
  { id: 17, title: 'Premante', genre: 'Comedy', rating: 6.2, year: 2025, description: 'Comedy film', posterUrl: '😂' },
  { id: 18, title: 'Mithra Mandali', genre: 'Comedy', rating: 5.0, year: 2025, description: 'Comedy film', posterUrl: '😂' },
  { id: 19, title: 'The Great Pre-Wedding Show', genre: 'Comedy', rating: 7.0, year: 2025, description: 'Comedy film', posterUrl: '😂' },
  
  // Action Movies
  { id: 20, title: 'Mana Shankara Varaprasad Garu', genre: 'Action', rating: 5.9, year: 2025, description: 'Action film', posterUrl: '⚡' },
  { id: 21, title: 'The Raja Saab', genre: 'Action', rating: 3.4, year: 2025, description: 'Action film', posterUrl: '⚡' },
  { id: 22, title: 'Akhanda 2', genre: 'Action', rating: 5.5, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 23, title: 'They Call Him OG', genre: 'Action', rating: 6.0, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 24, title: 'Champion', genre: 'Action', rating: 6.3, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 25, title: 'Mirai', genre: 'Action', rating: 7.1, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 26, title: 'Daaku Maharaaj', genre: 'Action', rating: 5.9, year: 2023, description: 'Action film', posterUrl: '⚡' },
  { id: 27, title: 'Game Changer', genre: 'Action', rating: 5.1, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 28, title: 'Kuberaa', genre: 'Action', rating: 6.4, year: 2024, description: 'Action film', posterUrl: '⚡' },
  { id: 29, title: 'HIT: The Third Case', genre: 'Action', rating: 6.9, year: 2024, description: 'Action film', posterUrl: '⚡' },
  
  // Romance Movies
  { id: 30, title: 'Couple Friendly', genre: 'Romance', rating: 6.8, year: 2024, description: 'Romance film', posterUrl: '💕' },
  { id: 31, title: 'Little Hearts', genre: 'Romance', rating: 7.6, year: 2024, description: 'Romance film', posterUrl: '💕' },
  { id: 32, title: 'Telusu Kada', genre: 'Romance', rating: 6.8, year: 2024, description: 'Romance film', posterUrl: '💕' },
  { id: 33, title: 'The Girlfriend', genre: 'Romance', rating: 6.6, year: 2024, description: 'Romance film', posterUrl: '💕' },
  { id: 34, title: 'K-Ramp', genre: 'Romance', rating: 7.1, year: 2024, description: 'Romance film', posterUrl: '💕' },
  { id: 35, title: 'Siddharth Roy', genre: 'Romance', rating: 6.2, year: 2024, description: 'Romance film', posterUrl: '💕' },
];

export default function WatchPage({ params }: { params: { id: string } }) {
  const [movie, setMovie] = useState<Movie | null>(null);

  useEffect(() => {
    const movieId = parseInt(params.id, 10);
    const foundMovie = allMovies.find((m) => m.id === movieId);
    setMovie(foundMovie || null);
  }, [params.id]);

  if (!movie) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <h1 className="text-2xl font-bold text-foreground">Movie Not Found</h1>
          <p className="text-muted-foreground">Sorry, we couldn't find that movie.</p>
          <Link href="/">
            <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const ratingColor =
    movie.rating >= 8.5
      ? 'text-accent'
      : movie.rating >= 7.5
        ? 'text-yellow-500'
        : 'text-orange-500';

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/">
            <Button variant="ghost" className="gap-2 text-accent hover:text-accent hover:bg-accent/10">
              ← Back
            </Button>
          </Link>
          <h1 className="text-xl font-bold text-foreground text-center flex-1">Watch Movie</h1>
          <div className="w-16"></div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-12">
        <Card className="bg-card border-2 border-card overflow-hidden">
          {/* Movie Poster */}
          <div className="w-full aspect-video bg-secondary/50 flex items-center justify-center text-9xl">
            {movie.posterUrl || '🎬'}
          </div>

          {/* Movie Info */}
          <div className="p-8 space-y-6">
            {/* Title and Rating */}
            <div className="space-y-3">
              <h1 className="text-4xl font-bold text-foreground">{movie.title}</h1>
              <div className="flex items-center gap-4 flex-wrap">
                <div className="flex items-center gap-2">
                  <span className={`text-3xl font-bold ${ratingColor}`}>
                    {movie.rating}/10
                  </span>
                </div>
                <div className="px-4 py-2 bg-primary/20 border border-primary rounded-lg">
                  <p className="text-sm font-medium text-primary">{movie.genre}</p>
                </div>
                <div className="px-4 py-2 bg-accent/20 border border-accent rounded-lg">
                  <p className="text-sm font-medium text-accent">Released: {movie.year}</p>
                </div>
              </div>
            </div>

            {/* Description */}
            <div className="space-y-2 border-t border-border pt-6">
              <h2 className="text-lg font-semibold text-foreground">Description</h2>
              <p className="text-muted-foreground leading-relaxed">
                {movie.description}
              </p>
            </div>

            {/* Movie Details */}
            <div className="grid grid-cols-2 gap-4 border-t border-border pt-6">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Genre</p>
                <p className="text-lg font-semibold text-foreground">{movie.genre}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Release Year</p>
                <p className="text-lg font-semibold text-foreground">{movie.year}</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 pt-6 border-t border-border">
              <button className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground py-3 rounded-lg font-semibold transition-colors">
                Play
              </button>
              <Link href="/" className="flex-1">
                <button className="w-full bg-secondary hover:bg-secondary/80 text-foreground py-3 rounded-lg font-semibold transition-colors">
                  View More Recommendations
                </button>
              </Link>
            </div>
          </div>
        </Card>
      </main>
    </div>
  );
}
