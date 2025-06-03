
import { useState } from "react";
import { VoiceRecorder } from "@/components/VoiceRecorder";
import { VideoGenerator } from "@/components/VideoGenerator";
import { ChatGPTFeed } from "@/components/ChatGPTFeed";
import { FullScreenIframe } from "@/components/FullScreenIframe";
import { Toaster } from "@/components/ui/toaster";

export interface UploadedImage {
  id: string;
  file: File;
  preview: string;
  name: string;
}

export interface VideoRequest {
  prompt: string;
  motion_bucket_id: number;
  cond_aug: number;
  steps: number;
  deep_cache: string;
  fps: number;
  negative_prompt: string;
  video_size: string;
}

const Index = () => {
  const [uploadedImages, setUploadedImages] = useState<UploadedImage[]>([]);
  const [voicePrompt, setVoicePrompt] = useState<string>("");
  const [isRecording, setIsRecording] = useState(false);
  const [isChatGPTFeedComplete, setIsChatGPTFeedComplete] = useState(false);
  const [showIframe, setShowIframe] = useState(false);

  const handleChatGPTFeedComplete = () => {
    setIsChatGPTFeedComplete(true);
    setShowIframe(true);
  };

  const handleIframeClose = () => {
    setShowIframe(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-800 via-slate-900 to-gray-900 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-r from-blue-500/10 to-indigo-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-l from-cyan-500/10 to-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-indigo-400 bg-clip-text text-transparent mb-4">
            SmartHousing
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Get AI enhanced properties information with stunning property video tours with AI-powered narration for real estate professionals
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Left Column - Property Market Data */}
          {/* <div className="space-y-6">
            <ChatGPTFeed onFeedComplete={handleChatGPTFeedComplete} />
          </div> */}

          {/* Right Column - Property Description & Video */}
          <div className="space-y-12">
            <VoiceRecorder 
              voicePrompt={voicePrompt}
              setVoicePrompt={setVoicePrompt}
              isRecording={isRecording}
              setIsRecording={setIsRecording}
            />
            
            <VideoGenerator 
              uploadedImages={uploadedImages}
              voicePrompt={voicePrompt}
              isEnabled={isChatGPTFeedComplete && !showIframe}
            />
          </div>
        </div>
      </div>

      {/* Full Screen Property Tour */}
      {showIframe && (
        <FullScreenIframe onClose={handleIframeClose} />
      )}

      <Toaster />
    </div>
  );
};

export default Index;
