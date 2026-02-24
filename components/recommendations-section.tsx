'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import MovieCard from '@/components/movie-card';
import { Spinner } from '@/components/ui/spinner';

interface Movie {
  id: number;
  title: string;
  genre: string;
  rating: number;
  year: number;
  description: string;
  posterUrl?: string;
}

interface RecommendationsSectionProps {
  userName: string;
  emotion?: string;
  onRestart: () => void;
}

export default function RecommendationsSection({
  userName,
  emotion = 'neutral',
  onRestart,
}: RecommendationsSectionProps) {
  const [recommendations, setRecommendations] = useState<Movie[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [detectedEmotion, setDetectedEmotion] = useState(emotion);

  useEffect(() => {
    const fetchRecommendations = async () => {
      setIsLoading(true);
      try {
        const response = await fetch('/api/recommendations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: userName, emotion: detectedEmotion }),
        });

        if (response.ok) {
          const data = await response.json();
          setRecommendations(data.recommendations || mockRecommendations);
        } else {
          setRecommendations(mockRecommendations);
        }
      } catch (err) {
        console.error('Error fetching recommendations:', err);
        setRecommendations(mockRecommendations);
      } finally {
        setIsLoading(false);
      }
    };

    const timer = setTimeout(fetchRecommendations, 1000);
    return () => clearTimeout(timer);
  }, [userName, detectedEmotion]);

  return (
    <div className="w-full max-w-4xl space-y-8 animate-fade-in">
      <div className="space-y-2 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-foreground">
          Your Top Picks
        </h2>
        <p className="text-lg text-muted-foreground">
          Personalized recommendations for {userName}
        </p>
        {detectedEmotion && (
          <div className="inline-block mt-4 px-4 py-2 bg-accent/20 border border-accent rounded-full">
            <p className="text-sm font-medium text-accent">
              {detectedEmotion === 'happy' && '😊 Happy - Recommending Horror, Action & Love movies'}
              {detectedEmotion === 'angry' && '😠 Angry - Recommending Funny, Action & Love movies'}
              {detectedEmotion === 'neutral' && '😐 Neutral - Recommending movies from all categories'}
            </p>
          </div>
        )}
      </div>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-12 gap-4">
          <Spinner className="h-8 w-8" />
          <p className="text-muted-foreground">Analyzing your preferences...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((movie, index) => (
              <div
                key={movie.id}
                className="animate-fade-in"
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <MovieCard movie={movie} rank={index + 1} />
              </div>
            ))}
          </div>

          {recommendations.length === 0 && (
            <Card className="p-8 text-center bg-secondary/50 border-2 border-accent/20">
              <p className="text-muted-foreground mb-4">No recommendations yet</p>
              <p className="text-sm text-muted-foreground">
                Try rating some movies first to get personalized recommendations
              </p>
            </Card>
          )}
        </>
      )}

      <div className="flex flex-col sm:flex-row gap-3 pt-4">
        <Button
          variant="outline"
          onClick={onRestart}
          className="flex-1 h-12 border-2 border-muted hover:border-accent text-foreground"
        >
          New User
        </Button>
        <Button
          className="flex-1 h-12 bg-accent hover:bg-accent/90 text-accent-foreground font-bold"
          onClick={() => {
            alert('Rate movies to improve recommendations!');
          }}
        >
          Rate Movies
        </Button>
      </div>
    </div>
  );
}

const mockRecommendations: Movie[] = [
  {
    id: 1,
    title: 'Inception',
    genre: 'Sci-Fi, Thriller',
    rating: 8.8,
    year: 2010,
    description: 'A thief who steals corporate secrets through dream-sharing',
    posterUrl: '🎬',
  },
  {
    id: 2,
    title: 'Interstellar',
    genre: 'Sci-Fi, Drama',
    rating: 8.7,
    year: 2014,
    description: 'Explorers travel through a wormhole to save humanity',
    posterUrl: '🌌',
  },
  {
    id: 3,
    title: 'The Dark Knight',
    genre: 'Action, Crime',
    rating: 9.0,
    year: 2008,
    description: 'When the menace known as the Joker wreaks havoc',
    posterUrl: '🦇',
  },
  {
    id: 4,
    title: 'Pulp Fiction',
    genre: 'Crime, Drama',
    rating: 8.9,
    year: 1994,
    description: 'The lives of two mob hitmen, a boxer and a pair',
    posterUrl: '🎞️',
  },
];
