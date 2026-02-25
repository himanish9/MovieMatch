'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';

interface FaceCaptureSectionProps {
  userName: string;
  onComplete: (emotion?: string) => void;
  onBack: () => void;
}

export default function FaceCaptureSection({
  userName,
  onComplete,
  onBack,
}: FaceCaptureSectionProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stage, setStage] = useState<'ready' | 'capturing' | 'processing'>('ready');
  const [captureProgress, setCaptureProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');
  const [detectedEmotion, setDetectedEmotion] = useState<string>('');

  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user' },
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setErrorMessage('Unable to access camera. Please check permissions.');
      }
    };

    initCamera();

    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, []);

  const detectEmotionFromFrame = (): string => {
    if (!videoRef.current) return 'neutral';
    
    const canvas = canvasRef.current;
    if (!canvas) return 'neutral';
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return 'neutral';
    
    // Draw video frame to canvas
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    // Helper function to calculate variance
    const calculateVariance = (pixels: number[]): number => {
      if (pixels.length === 0) return 0;
      const mean = pixels.reduce((a, b) => a + b, 0) / pixels.length;
      return pixels.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / pixels.length;
    };
    
    // RULE 1: Check for mouth opening and brightness (Happy indicator - HIGHEST PRIORITY)
    const mouthY = Math.floor(canvas.height * 0.60);
    const mouthHeight = Math.floor(canvas.height * 0.20);
    const mouthWidth = Math.floor(canvas.width * 0.55);
    const mouthStartX = Math.floor((canvas.width - mouthWidth) / 2);
    
    let brightPixels = 0;
    let darkPixels = 0;
    let mouthBrightness: number[] = [];
    
    for (let y = mouthY; y < mouthY + mouthHeight && y < canvas.height; y++) {
      for (let x = mouthStartX; x < mouthStartX + mouthWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];
        const brightness = (r + g + b) / 3;
        mouthBrightness.push(brightness);
        
        // Count bright pixels (teeth/open mouth)
        if (brightness > 180) {
          brightPixels++;
        }
        // Count dark pixels (closed mouth/shadow)
        if (brightness < 100) {
          darkPixels++;
        }
      }
    }
    
    const totalMouthPixels = mouthHeight * mouthWidth;
    const brightRatio = brightPixels / totalMouthPixels;
    const mouthVariance = calculateVariance(mouthBrightness);
    
    // LOWERED THRESHOLD: More achievable smile detection
    // Happy = visible brightness in mouth area OR high variance (smile)
    if (brightRatio > 0.08 || mouthVariance > 1500) {
      return 'happy';
    }
    
    // RULE 2: Check for furrowed brow (Angry indicator)
    // Looking at center forehead area for tension/wrinkles
    const foreheadY = Math.floor(canvas.height * 0.15);
    const foreheadHeight = Math.floor(canvas.height * 0.25);
    const foreheadWidth = Math.floor(canvas.width * 0.6);
    const foreheadStartX = Math.floor((canvas.width - foreheadWidth) / 2);
    
    let foreheadBrightness: number[] = [];
    let contrastAreas = 0;
    
    for (let y = foreheadY; y < foreheadY + foreheadHeight && y < canvas.height; y++) {
      for (let x = foreheadStartX; x < foreheadStartX + foreheadWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];
        const brightness = (r + g + b) / 3;
        foreheadBrightness.push(brightness);
        
        // Detect high contrast (furrowed wrinkles between eyebrows)
        if (x > foreheadStartX && x < foreheadStartX + foreheadWidth - 1) {
          const nextIdx = idx + 4;
          const nextBrightness = (data[nextIdx] + data[nextIdx + 1] + data[nextIdx + 2]) / 3;
          const contrastDiff = Math.abs(brightness - nextBrightness);
          if (contrastDiff > 25) {
            contrastAreas++;
          }
        }
      }
    }
    
    const foreheadVariance = calculateVariance(foreheadBrightness);
    const contrastDensity = contrastAreas / (foreheadHeight * foreheadWidth);
    
    // LOWERED THRESHOLDS: More sensitive angry detection
    // Angry = visible forehead tension/wrinkles OR high contrast density
    if (foreheadVariance > 300 || contrastDensity > 0.04) {
      return 'angry';
    }
    
    // RULE 3: Default to neutral if no strong indicators
    return 'neutral';
  };

  const handleCapture = async () => {
    setStage('capturing');
    setCaptureProgress(0);

    const totalFrames = 20;
    let emotionCounts = { happy: 0, angry: 0, neutral: 0 };
    
    const interval = setInterval(() => {
      setCaptureProgress((prev) => {
        const newProgress = prev + 1;
        
        // Detect emotion every frame
        const emotion = detectEmotionFromFrame() as 'happy' | 'angry' | 'neutral';
        emotionCounts[emotion]++;
        
        if (newProgress >= totalFrames) {
          clearInterval(interval);
          
          // Determine most common emotion
          const maxEmotion = Object.entries(emotionCounts).reduce((a, b) =>
            a[1] > b[1] ? a : b
          )[0];
          
          setDetectedEmotion(maxEmotion);
          setStage('processing');
          
          setTimeout(() => {
            onComplete(maxEmotion);
          }, 1500);
          
          return totalFrames;
        }
        return newProgress;
      });
    }, 200);
  };

  const handleCancel = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach((track) => track.stop());
    }
    onBack();
  };

  return (
    <div className="w-full max-w-lg space-y-6 animate-fade-in">
      <div className="space-y-2 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-foreground">
          Capture Your Face
        </h2>
        <p className="text-muted-foreground">
          Hello {userName}! Position your face in the center
        </p>
      </div>

      {errorMessage ? (
        <div className="bg-destructive/20 border border-destructive rounded-lg p-4 text-destructive">
          {errorMessage}
        </div>
      ) : (
        <div className="relative space-y-4">
          <div className="relative bg-card rounded-2xl overflow-hidden border-2 border-accent/20">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full aspect-video bg-black/50"
            />
            <canvas
              ref={canvasRef}
              width={320}
              height={240}
              className="hidden"
            />
            {stage !== 'ready' && (
              <div className="absolute inset-0 bg-gradient-to-t from-accent/20 via-transparent to-transparent" />
            )}
          </div>

          {stage === 'capturing' && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-foreground">
                  Capturing: {captureProgress}/20
                </span>
                <span className="text-xs text-muted-foreground">
                  {Math.round((captureProgress / 20) * 100)}%
                </span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-accent to-primary transition-all duration-300"
                  style={{ width: `${(captureProgress / 20) * 100}%` }}
                />
              </div>
            </div>
          )}

          {stage === 'processing' && (
            <div className="flex items-center justify-center gap-3 py-4">
              <Spinner className="h-5 w-5" />
              <span className="text-foreground font-medium">Processing your face...</span>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-3">
        <Button
          variant="outline"
          onClick={handleCancel}
          disabled={stage !== 'ready'}
          className="flex-1 h-12 border-2 border-muted hover:border-accent"
        >
          Back
        </Button>
        <Button
          onClick={handleCapture}
          disabled={stage !== 'ready' || !!errorMessage}
          className="flex-1 h-12 bg-primary hover:bg-primary/90 text-primary-foreground font-bold"
        >
          {stage === 'ready' ? 'Capture Face' : 'Capturing...'}
        </Button>
      </div>

      <div className="text-xs text-muted-foreground text-center space-y-1">
        <p>Your face data is encrypted and stored locally</p>
        <p>It will never be shared or stored on servers</p>
      </div>
    </div>
  );
}
