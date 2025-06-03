
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Building2, ExternalLink } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const staticContent = {
  links: [
    { title: "Luxury Home Listings", url: "https://example.com/luxury", description: "Browse premium properties in your area" },
    { title: "Market Analysis Reports", url: "https://example.com/reports", description: "Current real estate market insights" },
    { title: "Property Investment Guide", url: "https://example.com/investment", description: "Investment strategies for real estate" },
    { title: "Virtual Tour Examples", url: "https://example.com/tours", description: "Sample property video tours" },
    { title: "Staging & Photography Tips", url: "https://example.com/staging", description: "How to prepare properties for sale" },
    { title: "Comparative Market Analysis", url: "https://example.com/cma", description: "Property valuation tools" }
  ],
  images: [
    { id: 1, url: "https://images.unsplash.com/photo-1721322800607-8c38375eef04", title: "Modern Living Room" },
    { id: 2, url: "https://images.unsplash.com/photo-1487958449943-2429e8be8625", title: "Contemporary Exterior" },
    { id: 3, url: "https://images.unsplash.com/photo-1649972904349-6e44c42644a7", title: "Kitchen & Dining" },
    { id: 4, url: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158", title: "Home Office Space" },
    { id: 5, url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2", title: "Master Bedroom" },
    { id: 6, url: "https://images.unsplash.com/photo-1571055107559-3e67626fa8be", title: "Outdoor Living Area" }
  ]
};

interface ChatGPTFeedProps {
  onFeedComplete?: () => void;
}

export const ChatGPTFeed = ({ onFeedComplete }: ChatGPTFeedProps) => {
  const [showContent, setShowContent] = useState(false);
  const [isFeeding, setIsFeeding] = useState(false);

  const handleFeedToChatGPT = async () => {
    setIsFeeding(true);
    
    // Simulate feeding property data to ChatGPT
    setTimeout(() => {
      setIsFeeding(false);
      setShowContent(false);
      toast({
        title: "Market Data Processed",
        description: "Property market data has been analyzed and resources are now available.",
      });
      
      // Call the completion callback after a short delay
      setTimeout(() => {
        if (onFeedComplete) {
          onFeedComplete();
        }
      }, 1000);
    }, 2000);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500">
          <Building2 className="h-5 w-5 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white">Market Intelligence</h2>
      </div>

      {/* Feed Button */}
      <Button
        onClick={handleFeedToChatGPT}
        disabled={isFeeding}
        className="w-full h-12 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mb-6"
      >
        {isFeeding ? (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            Analyzing Market Data...
          </div>
        ) : (
          "🏘️ Load Property Market Data"
        )}
      </Button>

      {/* Static Content Display */}
      {showContent && (
        <div className="space-y-6 animate-fade-in">
          {/* Links Section */}
          <div>
            <h3 className="text-lg font-medium text-white mb-4">Real Estate Resources</h3>
            <div className="space-y-3">
              {staticContent.links.map((link, index) => (
                <div key={index} className="bg-white/5 rounded-lg p-3 border border-white/10 hover:border-blue-400/50 transition-all duration-300">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-white font-medium">{link.title}</h4>
                      <p className="text-gray-400 text-sm">{link.description}</p>
                    </div>
                    <ExternalLink className="h-4 w-4 text-blue-400" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Images Section */}
          <div>
            <h3 className="text-lg font-medium text-white mb-4">Property Showcase</h3>
            <div className="grid grid-cols-2 gap-3">
              {staticContent.images.map((image) => (
                <div key={image.id} className="relative group bg-white/5 rounded-lg overflow-hidden border border-white/10 hover:border-blue-400/50 transition-all duration-300">
                  <img
                    src={image.url}
                    alt={image.title}
                    className="w-full h-24 object-cover"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <p className="text-white text-xs font-medium text-center px-2">{image.title}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
