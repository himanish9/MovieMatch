'use client';

import { useState } from 'react';
import NameInputForm from '@/components/name-input-form';
import FaceCaptureSection from '@/components/face-capture-section';
import RecommendationsSection from '@/components/recommendations-section';
import Header from '@/components/header';

type Stage = 'name' | 'face' | 'recommendations';

export default function Home() {
  const [stage, setStage] = useState<Stage>('name');
  const [userName, setUserName] = useState<string>('');
  const [detectedEmotion, setDetectedEmotion] = useState<string>('neutral');

  const handleNameSubmit = (name: string) => {
    setUserName(name);
    setStage('face');
  };

  const handleFaceCapture = (emotion: string = 'neutral') => {
    setDetectedEmotion(emotion);
    setStage('recommendations');
  };

  const handleRestart = () => {
    setStage('name');
    setUserName('');
    setDetectedEmotion('neutral');
  };

  return (
    <main className="min-h-screen bg-background">
      {stage === 'name' && (
        <div className="fixed inset-0 -z-10 overflow-hidden">
          <div
            className="absolute inset-0 opacity-50"
            style={{
              backgroundImage: `url('/cinema-background.jpg')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          />
          <div className="absolute inset-0 bg-black/40" />
        </div>
      )}

      <Header />

      <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
        {stage === 'name' && (
          <NameInputForm onSubmit={handleNameSubmit} />
        )}

        {stage === 'face' && (
          <FaceCaptureSection
            userName={userName}
            onComplete={handleFaceCapture}
            onBack={() => setStage('name')}
          />
        )}

        {stage === 'recommendations' && (
          <RecommendationsSection
            userName={userName}
            emotion={detectedEmotion}
            onRestart={handleRestart}
          />
        )}
      </div>
    </main>
  );
}
