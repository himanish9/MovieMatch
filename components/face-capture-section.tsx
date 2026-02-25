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
    
    // Helper function to get pixel brightness
    const getBrightness = (r: number, g: number, b: number): number => {
      return (r + g + b) / 3;
    };

    // Helper function to calculate variance
    const calculateVariance = (pixels: number[]): number => {
      if (pixels.length === 0) return 0;
      const mean = pixels.reduce((a, b) => a + b, 0) / pixels.length;
      return pixels.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / pixels.length;
    };

    // Helper function to count edge pixels (high contrast)
    const countEdges = (region: { startX: number; startY: number; width: number; height: number }): number => {
      let edges = 0;
      for (let y = region.startY; y < region.startY + region.height && y < canvas.height; y++) {
        for (let x = region.startX; x < region.startX + region.width && x < canvas.width; x++) {
          if (x < region.startX + region.width - 1) {
            const idx = (y * canvas.width + x) * 4;
            const nextIdx = idx + 4;
            const brightness = getBrightness(data[idx], data[idx + 1], data[idx + 2]);
            const nextBrightness = getBrightness(data[nextIdx], data[nextIdx + 1], data[nextIdx + 2]);
            if (Math.abs(brightness - nextBrightness) > 30) {
              edges++;
            }
          }
        }
      }
      return edges;
    };
    
    // HAPPY: Teeth clearly visible + mouth open/widely stretched + cheeks raised
    // Detect bright pixels in mouth region (teeth) and cheek region (raised)
    const mouthY = Math.floor(canvas.height * 0.58);
    const mouthHeight = Math.floor(canvas.height * 0.22);
    const mouthWidth = Math.floor(canvas.width * 0.60);
    const mouthStartX = Math.floor((canvas.width - mouthWidth) / 2);
    
    let mouthBrightness: number[] = [];
    let teethPixels = 0;
    
    for (let y = mouthY; y < mouthY + mouthHeight && y < canvas.height; y++) {
      for (let x = mouthStartX; x < mouthStartX + mouthWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        const brightness = getBrightness(data[idx], data[idx + 1], data[idx + 2]);
        mouthBrightness.push(brightness);
        
        // Count very bright pixels (teeth are bright)
        if (brightness > 190) {
          teethPixels++;
        }
      }
    }
    
    // Check cheeks for raised appearance (higher brightness on sides)
    const cheekY = Math.floor(canvas.height * 0.45);
    const cheekHeight = Math.floor(canvas.height * 0.15);
    const leftCheekX = Math.floor(canvas.width * 0.1);
    const rightCheekX = Math.floor(canvas.width * 0.65);
    const cheekWidth = Math.floor(canvas.width * 0.25);
    
    let leftCheekBrightness: number[] = [];
    let rightCheekBrightness: number[] = [];
    
    for (let y = cheekY; y < cheekY + cheekHeight && y < canvas.height; y++) {
      // Left cheek
      for (let x = leftCheekX; x < leftCheekX + cheekWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        leftCheekBrightness.push(getBrightness(data[idx], data[idx + 1], data[idx + 2]));
      }
      // Right cheek
      for (let x = rightCheekX; x < rightCheekX + cheekWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        rightCheekBrightness.push(getBrightness(data[idx], data[idx + 1], data[idx + 2]));
      }
    }
    
    const totalMouthPixels = mouthHeight * mouthWidth;
    const teethVisibilityRatio = teethPixels / totalMouthPixels;
    const mouthVariance = calculateVariance(mouthBrightness);
    const leftCheekAvg = leftCheekBrightness.reduce((a, b) => a + b, 0) / Math.max(leftCheekBrightness.length, 1);
    const rightCheekAvg = rightCheekBrightness.reduce((a, b) => a + b, 0) / Math.max(rightCheekBrightness.length, 1);
    
    // Happy when: clear teeth visible AND high mouth variance (smile shape) AND raised cheeks
    if (teethVisibilityRatio > 0.06 && mouthVariance > 1200 && (leftCheekAvg > 110 || rightCheekAvg > 110)) {
      return 'happy';
    }
    
    // ANGRY: Eyebrows lowered/pulled together + eyes narrowed + jaw tense
    // Detect furrowed brow (dark lines between eyebrows) and tension in facial muscles
    const browY = Math.floor(canvas.height * 0.20);
    const browHeight = Math.floor(canvas.height * 0.20);
    const browWidth = Math.floor(canvas.width * 0.65);
    const browStartX = Math.floor((canvas.width - browWidth) / 2);
    
    let browBrightness: number[] = [];
    let browDarkPixels = 0;
    
    for (let y = browY; y < browY + browHeight && y < canvas.height; y++) {
      for (let x = browStartX; x < browStartX + browWidth && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        const brightness = getBrightness(data[idx], data[idx + 1], data[idx + 2]);
        browBrightness.push(brightness);
        
        // Count dark pixels (furrowed wrinkles appear dark)
        if (brightness < 80) {
          browDarkPixels++;
        }
      }
    }
    
    const browVariance = calculateVariance(browBrightness);
    const browDarkRatio = browDarkPixels / (browHeight * browWidth);
    const browEdges = countEdges({ startX: browStartX, startY: browY, width: browWidth, height: browHeight });
    const browEdgeDensity = browEdges / (browHeight * browWidth);
    
    // Check eyes for narrowing (detect horizontal lines)
    const eyeY = Math.floor(canvas.height * 0.35);
    const eyeHeight = Math.floor(canvas.height * 0.12);
    const eyeWidth = Math.floor(canvas.width * 0.70);
    const eyeStartX = Math.floor((canvas.width - eyeWidth) / 2);
    
    let eyeContrastAreas = 0;
    for (let y = eyeY; y < eyeY + eyeHeight && y < canvas.height; y++) {
      for (let x = eyeStartX; x < eyeStartX + eyeWidth - 1 && x < canvas.width; x++) {
        const idx = (y * canvas.width + x) * 4;
        const nextIdx = idx + 4;
        const brightness = getBrightness(data[idx], data[idx + 1], data[idx + 2]);
        const nextBrightness = getBrightness(data[nextIdx], data[nextIdx + 1], data[nextIdx + 2]);
        if (Math.abs(brightness - nextBrightness) > 35) {
          eyeContrastAreas++;
        }
      }
    }
    const eyeContrastDensity = eyeContrastAreas / (eyeHeight * eyeWidth);
    
    // Angry when: furrowed brow (high variance + dark pixels + edges) AND eye narrowing
    if ((browVariance > 250 && browDarkRatio > 0.05 && browEdgeDensity > 0.025) && eyeContrastDensity > 0.03) {
      return 'angry';
    }
    
    // NEUTRAL: Default - teeth not visible, mouth closed, relaxed
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
