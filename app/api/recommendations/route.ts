import { NextRequest, NextResponse } from 'next/server';

const genreEmojis: { [key: string]: string } = {
  Comedy: '😂',
  Horror: '👻',
  Action: '⚡',
  Romance: '💕',
};

const mockMovies = [
  // Horror Movies
  { id: 1, title: 'Kishkindhapuri', genre: 'Horror', rating: 6.9, description: 'Horror film', posterUrl: '👻' },
  { id: 2, title: 'Ghatikachalam', genre: 'Horror', rating: 6.1, description: 'Horror film', posterUrl: '👻' },
  { id: 3, title: 'Subham', genre: 'Horror', rating: 7.2, description: 'Horror film', posterUrl: '👻' },
  { id: 4, title: 'Jatadhara', genre: 'Horror', rating: 3.3, description: 'Horror film', posterUrl: '👻' },
  { id: 5, title: 'Odela 2', genre: 'Horror', rating: 4.6, description: 'Horror film', posterUrl: '👻' },
  { id: 6, title: 'Eesha', genre: 'Horror', rating: 9.1, description: 'Horror film', posterUrl: '👻' },
  { id: 7, title: 'Kalinga', genre: 'Horror', rating: 6.6, description: 'Horror film', posterUrl: '👻' },
  { id: 8, title: 'Demonte Colony 2', genre: 'Horror', rating: 6.5, description: 'Horror film', posterUrl: '👻' },
  { id: 9, title: 'Geethanjali Malli Vachindi', genre: 'Horror', rating: 4.7, description: 'Horror film', posterUrl: '👻' },
  { id: 10, title: 'Tantra', genre: 'Horror', rating: 4.9, description: 'Horror film', posterUrl: '👻' },
  
  // Comedy Movies
  { id: 11, title: 'Mathu Vadalara 2', genre: 'Comedy', rating: 8.2, description: 'Comedy film', posterUrl: '😂' },
  { id: 12, title: 'Aay', genre: 'Comedy', rating: 7.5, description: 'Comedy film', posterUrl: '😂' },
  { id: 13, title: 'Maruthi Nagar Subramanyam', genre: 'Comedy', rating: 7.2, description: 'Comedy film', posterUrl: '😂' },
  { id: 14, title: '35 Chinna Katha Kaadu', genre: 'Comedy', rating: 7.8, description: 'Comedy film', posterUrl: '😂' },
  { id: 15, title: 'MAD', genre: 'Comedy', rating: 7.3, description: 'Comedy film', posterUrl: '😂' },
  { id: 16, title: 'Janaka Aithe Ganaka', genre: 'Comedy', rating: 6.5, description: 'Comedy film', posterUrl: '😂' },
  { id: 17, title: 'Premante', genre: 'Comedy', rating: 6.2, description: 'Comedy film', posterUrl: '😂' },
  { id: 18, title: 'Mithra Mandali', genre: 'Comedy', rating: 5.0, description: 'Comedy film', posterUrl: '😂' },
  { id: 19, title: 'The Great Pre-Wedding Show', genre: 'Comedy', rating: 7.0, description: 'Comedy film', posterUrl: '😂' },
  
  // Action Movies
  { id: 20, title: 'Mana Shankara Varaprasad Garu', genre: 'Action', rating: 5.9, description: 'Action film', posterUrl: '⚡' },
  { id: 21, title: 'The Raja Saab', genre: 'Action', rating: 3.4, description: 'Action film', posterUrl: '⚡' },
  { id: 22, title: 'Akhanda 2', genre: 'Action', rating: 5.5, description: 'Action film', posterUrl: '⚡' },
  { id: 23, title: 'They Call Him OG', genre: 'Action', rating: 6.0, description: 'Action film', posterUrl: '⚡' },
  { id: 24, title: 'Champion', genre: 'Action', rating: 6.3, description: 'Action film', posterUrl: '⚡' },
  { id: 25, title: 'Mirai', genre: 'Action', rating: 7.1, description: 'Action film', posterUrl: '⚡' },
  { id: 26, title: 'Daaku Maharaaj', genre: 'Action', rating: 5.9, description: 'Action film', posterUrl: '⚡' },
  { id: 27, title: 'Game Changer', genre: 'Action', rating: 5.1, description: 'Action film', posterUrl: '⚡' },
  { id: 28, title: 'Kuberaa', genre: 'Action', rating: 6.4, description: 'Action film', posterUrl: '⚡' },
  { id: 29, title: 'HIT: The Third Case', genre: 'Action', rating: 6.9, description: 'Action film', posterUrl: '⚡' },
  
  // Romance Movies
  { id: 30, title: 'Couple Friendly', genre: 'Romance', rating: 6.8, description: 'Romance film', posterUrl: '💕' },
  { id: 31, title: 'Little Hearts', genre: 'Romance', rating: 7.6, description: 'Romance film', posterUrl: '💕' },
  { id: 32, title: 'Telusu Kada', genre: 'Romance', rating: 6.8, description: 'Romance film', posterUrl: '💕' },
  { id: 33, title: 'The Girlfriend', genre: 'Romance', rating: 6.6, description: 'Romance film', posterUrl: '💕' },
  { id: 34, title: 'K-Ramp', genre: 'Romance', rating: 7.1, description: 'Romance film', posterUrl: '💕' },
  { id: 35, title: 'Siddharth Roy', genre: 'Romance', rating: 6.2, description: 'Romance film', posterUrl: '💕' },
];

export async function POST(request: NextRequest) {
  try {
    const { name, emotion = 'neutral' } = await request.json();

    if (!name || typeof name !== 'string') {
      return NextResponse.json(
        { error: 'Invalid name parameter' },
        { status: 400 }
      );
    }

    // Get emotion-based recommendations
    const recommendations = getEmotionBasedRecommendations(emotion);

    return NextResponse.json({
      success: true,
      userName: name,
      emotion,
      recommendations,
      message: `Top recommendations for ${name}`,
    });
  } catch (error) {
    console.error('Error generating recommendations:', error);
    return NextResponse.json(
      { error: 'Failed to generate recommendations' },
      { status: 500 }
    );
  }
}

function getEmotionBasedRecommendations(emotion: string) {
  const emotionLower = (emotion || 'neutral').toLowerCase();
  let selectedGenres: string[] = [];

  if (emotionLower === 'happy') {
    // Happy: Horror, Action, Romance
    selectedGenres = ['Horror', 'Action', 'Romance'];
  } else if (emotionLower === 'angry') {
    // Angry: Comedy, Action, Romance
    selectedGenres = ['Comedy', 'Action', 'Romance'];
  } else {
    // Neutral: All categories
    selectedGenres = ['Comedy', 'Horror', 'Action', 'Romance'];
  }

  // Filter movies by selected genres
  const filteredMovies = mockMovies.filter((movie) =>
    selectedGenres.includes(movie.genre)
  );

  // Sort by rating and get top 12+ movies
  return filteredMovies
    .sort((a, b) => b.rating - a.rating)
    .slice(0, 12);
}
