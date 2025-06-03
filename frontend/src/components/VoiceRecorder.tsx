
import { useState, useRef, useEffect } from "react";
import { Mic, MicOff, Home, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/hooks/use-toast";
import { Navigate } from 'react-router-dom';
interface VoiceRecorderProps {
  voicePrompt: string;
  setVoicePrompt: (prompt: string) => void;
  isRecording: boolean;
  setIsRecording: (recording: boolean) => void;
}

export const VoiceRecorder = ({ 
  voicePrompt, 
  setVoicePrompt, 
  isRecording, 
  setIsRecording 
}: VoiceRecorderProps) => {
  const [isListening, setIsListening] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [audioLevel, setAudioLevel] = useState(0);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Create audio context for visualization
      const audioContext = new AudioContext();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      microphone.connect(analyser);
      
      analyser.fftSize = 256;
      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      
      const updateAudioLevel = () => {
        analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        setAudioLevel(average);
        if (isRecording) {
          requestAnimationFrame(updateAudioLevel);
        }
      };
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setIsListening(true);
      updateAudioLevel();
      
      toast({
        title: "Recording started!",
        description: "Describe this property's key features and selling points.",
      });
      
      // Simulate speech recognition (in a real app, you'd use actual speech recognition)
      setTimeout(() => {
        if (isRecording) {
          setVoicePrompt("This stunning 3-bedroom home features an open floor plan, gourmet kitchen with granite countertops, hardwood floors throughout, and a beautiful backyard perfect for entertaining");
          stopRecording();
        }
      }, 5000);
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast({
        title: "Microphone Error",
        description: "Could not access microphone. Please check permissions.",
        variant: "destructive",
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
      setIsListening(false);
      setAudioLevel(0);
      
      toast({
        title: "Property description recorded!",
        description: "Your property description has been captured.",
      });
    }
  };

  const handleConfirm = () => {
    // Simulate transcription process
    setVoicePrompt("Find a three-bedroom house with a large backyard and modern kitchen in the downtown area.");
    toast({
      title: "C!",
      description: "Y property description has been converted to text.",
    });
    
  };
  
  function navigateToAbout() {
  window.location.href = '/about';
};
  const handleTranscribe = () => {
    // Simulate transcription process
    setVoicePrompt("This stunning 3-bedroom home features an open floor plan, gourmet kitchen with granite countertops, hardwood floors throughout, and a beautiful backyard perfect for entertaining");
    toast({
      title: "C!",
      description: "Y property description has been converted to text.",
    });
    
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500">
          <Home className="h-5 w-5 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white">Use your voice to ask the smart house about any properties</h2>
      </div>

      {/* Voice Recording Interface */}
      <div className="text-center mb-6">
        <div className="relative inline-block">
          {/* Animated rings for recording */}
          {isRecording && (
            <>
              <div className="absolute inset-0 rounded-full bg-blue-500/20 animate-ping"></div>
              <div className="absolute inset-0 rounded-full bg-blue-500/30 animate-pulse"></div>
            </>
          )}
          
          {/* Main record button */}
          <Button
            size="lg"
            onClick={isRecording ? stopRecording : startRecording}
            className={`h-20 w-20 rounded-full transition-all duration-300 ${
              isRecording 
                ? 'bg-red-500 hover:bg-red-600 shadow-red-500/50 shadow-lg scale-110' 
                : 'bg-gradient-to-r from-blue-500 to-indigo-500 hover:scale-105 shadow-blue-500/50 shadow-lg'
            }`}
          >
            {isRecording ? (
              <MicOff className="h-8 w-8 text-white" />
            ) : (
              <Mic className="h-8 w-8 text-white" />
            )}
          </Button>
        </div>

        {/* Audio visualization */}
        {isRecording && (
          <div className="mt-4 flex justify-center items-center gap-1">
            {Array.from({ length: 20 }).map((_, i) => (
              <div
                key={i}
                className="bg-gradient-to-t from-blue-500 to-indigo-500 rounded-full w-1 transition-all duration-100"
                style={{
                  height: `${Math.max(4, (audioLevel / 255) * 40 + Math.random() * 20)}px`,
                  animationDelay: `${i * 50}ms`
                }}
              />
            ))}
          </div>
        )}

        <p className="text-gray-300 mt-4">
          {isRecording 
            ? "🏠 Recording... Describe the property's best features!" 
            : "Click to record your property description"
          }
        </p>
      </div>

      {/* Transcribe Button */}
      <div className="flex justify-center mb-6">
        <Button
          onClick={handleTranscribe}
          disabled={isRecording}
          className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-semibold px-6 py-3 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FileText className="h-5 w-5 mr-2" />
          Translate
        </Button>
      </div>
      

      {/* Text prompt display/edit */}
      <div className="space-y-4">
        <label className="text-white font-medium">Property Description:</label>
        <Textarea
          value={voicePrompt}
          onChange={(e) => setVoicePrompt(e.target.value)}
          placeholder="Describe the property's key features, amenities, and selling points..."
          className="bg-white/5 border-white/20 text-white placeholder:text-gray-400 min-h-[100px] resize-none"
        />
      </div>
      
      <div className="flex justify-center mb-6">
        <Button
          onClick={navigateToAbout}
          disabled={isRecording}
          className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-semibold px-6 py-3 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FileText className="h-5 w-5 mr-2" />
          Confirm
        </Button>
      </div>
    </div>
  );
};
