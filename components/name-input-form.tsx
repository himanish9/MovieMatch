'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface NameInputFormProps {
  onSubmit: (name: string) => void;
}

export default function NameInputForm({ onSubmit }: NameInputFormProps) {
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      setIsLoading(true);
      setTimeout(() => {
        onSubmit(name.trim());
        setIsLoading(false);
      }, 300);
    }
  };

  return (
    <div className="w-full max-w-md space-y-8 text-center animate-fade-in">
      <div className="space-y-4">
        <h1 className="text-4xl sm:text-5xl font-bold text-foreground text-balance">
          🎬 Cinema Experience
        </h1>
        <h2 className="text-2xl sm:text-3xl font-semibold text-primary mb-6">
          Enter Your Name
        </h2>
        <p className="text-lg text-muted-foreground">
          Get personalized movie recommendations based on your face
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <Input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus
            className="h-14 px-6 bg-card border-2 border-card hover:border-accent focus:border-accent focus:ring-2 focus:ring-accent/20 rounded-full text-base placeholder-muted-foreground transition-all"
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e as any)}
            disabled={isLoading}
          />
        </div>

        <Button
          type="submit"
          disabled={!name.trim() || isLoading}
          className="w-full h-14 bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg rounded-full shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Loading...' : 'Start'}
        </Button>
      </form>

      <div className="pt-8 space-y-2 text-sm text-muted-foreground">
        <p>Your face will be captured and used for</p>
        <p>personalized recommendations</p>
      </div>
    </div>
  );
}
