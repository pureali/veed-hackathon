
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";
import { UploadedImage } from "@/pages/Index";

interface ImageUploadProps {
  uploadedImages: UploadedImage[];
  setUploadedImages: (images: UploadedImage[]) => void;
}

export const ImageUpload = ({ uploadedImages, setUploadedImages }: ImageUploadProps) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newImages: UploadedImage[] = acceptedFiles.map((file) => ({
      id: Math.random().toString(36).substring(7),
      file,
      preview: URL.createObjectURL(file),
      name: file.name,
    }));

    setUploadedImages([...uploadedImages, ...newImages]);
    toast({
      title: "Images uploaded successfully!",
      description: `Added ${acceptedFiles.length} image(s) to your collection.`,
    });
  }, [uploadedImages, setUploadedImages]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    multiple: true
  });

  const removeImage = (id: string) => {
    const imageToRemove = uploadedImages.find(img => img.id === id);
    if (imageToRemove) {
      URL.revokeObjectURL(imageToRemove.preview);
    }
    setUploadedImages(uploadedImages.filter(img => img.id !== id));
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500">
          <Home className="h-5 w-5 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white">Upload Property Images</h2>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragActive
            ? 'border-amber-400 bg-amber-500/20 scale-105'
            : 'border-gray-400 hover:border-amber-400 hover:bg-amber-500/10'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-4">
          <div className={`p-4 rounded-full transition-all duration-300 ${
            isDragActive ? 'bg-amber-500 scale-110' : 'bg-gray-600'
          }`}>
            <Upload className="h-8 w-8 text-white" />
          </div>
          <div>
            <p className="text-lg text-white font-medium mb-2">
              {isDragActive ? 'Drop your property images here!' : 'Drag & drop property images here'}
            </p>
            <p className="text-gray-300 text-sm">
              or <span className="text-amber-400 font-medium">browse files</span>
            </p>
          </div>
        </div>
      </div>

      {/* Uploaded Images Grid */}
      {uploadedImages.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-white mb-4">
            Property Images ({uploadedImages.length})
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {uploadedImages.map((image) => (
              <div
                key={image.id}
                className="relative group bg-white/5 rounded-lg overflow-hidden border border-white/10 hover:border-amber-400/50 transition-all duration-300"
              >
                <img
                  src={image.preview}
                  alt={image.name}
                  className="w-full h-24 object-cover"
                />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => removeImage(image.id)}
                    className="h-8 w-8 p-0"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                <div className="p-2">
                  <p className="text-xs text-gray-300 truncate">{image.name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
