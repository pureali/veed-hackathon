
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { X, ExternalLink } from "lucide-react";

interface FullScreenIframeProps {
  onClose: () => void;
}

export const FullScreenIframe = ({ onClose }: FullScreenIframeProps) => {
  const [isLoading, setIsLoading] = useState(true);

  const handleIframeLoad = () => {
    setIsLoading(false);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm animate-fade-in">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 bg-gradient-to-r from-amber-500/20 to-orange-500/20 backdrop-blur-lg border-b border-white/10">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3">
            <ExternalLink className="h-6 w-6 text-amber-400" />
            <h2 className="text-xl font-semibold text-white">Property Analytics Dashboard</h2>
          </div>
          <Button
            onClick={onClose}
            variant="ghost"
            className="text-white hover:bg-white/10 h-10 w-10 p-0"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-amber-400/30 border-t-amber-400 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-white text-lg">Loading property data...</p>
          </div>
        </div>
      )}

      {/* Iframe */}
      <iframe
        src="https://example.com"
        className="w-full h-full pt-20"
        frameBorder="0"
        allowFullScreen
        onLoad={handleIframeLoad}
        title="Property Analytics Dashboard"
      />

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
        <div className="text-center">
          <p className="text-gray-300 text-sm">
            Review the property analytics above, then proceed to generate your video tour
          </p>
          <Button
            onClick={onClose}
            className="mt-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-semibold px-6 py-2 rounded-lg"
          >
            Continue to Video Generation
          </Button>
        </div>
      </div>
    </div>
  );
};
