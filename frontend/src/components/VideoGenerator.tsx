
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { toast } from "@/hooks/use-toast";
import { UploadedImage, VideoRequest } from "@/pages/Index";
import { useQuery } from "@tanstack/react-query";
import { Video, Home } from "lucide-react";

interface Voice {
  voice_id: string;
  name: string;
  category: string;
  description: string;
  preview_url: string;
}

interface VideoGeneratorProps {
  uploadedImages: UploadedImage[];
  voicePrompt: string;
  isEnabled?: boolean;
}

export const VideoGenerator = ({ uploadedImages, voicePrompt, isEnabled = true }: VideoGeneratorProps) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);

  // Default video settings optimized for real estate
  const defaultVideoSettings = {
    motion_bucket_id: 127,
    cond_aug: 0.02,
    steps: 20,
    fps: 10,
    video_size: "landscape_16_9"
  };

  // Fetch available voices
  const { data: voices, isLoading: voicesLoading } = useQuery({
    queryKey: ['voices'],
    queryFn: async (): Promise<Voice[]> => {
      const response = await fetch('http://0.0.0.0:8001/voices/');
      if (!response.ok) {
        throw new Error('Failed to fetch voices');
      }
      return response.json();
    },
  });

  const generateVideo = async () => {
    if (!voicePrompt.trim()) {
      toast({
        title: "Missing Property Description",
        description: "Please provide a description for your property listing video.",
        variant: "destructive",
      });
      return;
    }

    setIsGenerating(true);
    setProgress(0);

    try {
      const videoRequest: VideoRequest = {
        prompt: voicePrompt,
        motion_bucket_id: defaultVideoSettings.motion_bucket_id,
        cond_aug: defaultVideoSettings.cond_aug,
        steps: defaultVideoSettings.steps,
        deep_cache: "none",
        fps: defaultVideoSettings.fps,
        negative_prompt: "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
        video_size: defaultVideoSettings.video_size
      };

      console.log('Generating property listing video with request:', videoRequest);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + Math.random() * 10;
        });
      }, 500);

      const response = await fetch('http://0.0.0.0:8001/generate_video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(videoRequest),
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        throw new Error('Failed to generate property listing video');
      }

      const result = await response.json();
      console.log('Property listing video generation result:', result);

      toast({
        title: "Property Video Created!",
        description: "Your professional property listing video is ready to view.",
      });

    } catch (error) {
      console.error('Error generating property listing video:', error);
      toast({
        title: "Generation Failed",
        description: "There was an error creating your property video. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
      setProgress(0);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500">
          <Video className="h-5 w-5 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white">Property Video Creation</h2>
      </div>

      {/* Available Voices Display */}
      {voicesLoading ? (
        <div className="text-gray-300 text-center py-4">Loading professional voice options...</div>
      ) : voices && voices.length > 0 ? (
        <div className="mb-6">
          <h3 className="text-white font-medium mb-3">Professional Narrator Voices ({voices.length})</h3>
          <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto">
            {voices.map((voice) => (
              <div key={voice.voice_id} className="bg-white/5 rounded-lg p-2 text-xs">
                <p className="text-white font-medium">{voice.name}</p>
                <p className="text-gray-400">{voice.category}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Generation Progress */}
      {isGenerating && (
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-medium">Creating Property Listing Video...</span>
            <span className="text-blue-400">{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
          <p className="text-xs text-gray-400 mt-2">Crafting your professional property presentation</p>
        </div>
      )}

      {/* Generate Button */}
      <Button
        onClick={generateVideo}
        disabled={isGenerating || !voicePrompt.trim() || !isEnabled}
        className="w-full h-12 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isGenerating ? (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            Creating Property Video...
          </div>
        ) : !isEnabled ? (
          "Complete Previous Steps First"
        ) : (
          <div className="flex items-center gap-2">
            <Home className="h-5 w-5" />
            See the Property Video
          </div>
        )}
      </Button>

      {/* Status Info */}
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-400">
          {voicePrompt ? "Property description ready" : "Waiting for property description"} • {isEnabled ? "Ready to generate" : "Complete market data loading first"}
        </p>
      </div>
    </div>
  );
};
