interface IconButtonProps {
  icon: React.ReactNode; // Accepts any valid React node, like an SVG
  onClick?: () => void; // Optional click handler
}

const IconButton = ({ icon, onClick }: IconButtonProps) => {
  return (
    <button
      onClick={onClick} // Attach the onClick event
      className="inline-flex h-20 w-20 items-center justify-center rounded-full bg-gray-50 text-black drop-shadow-sm transition-colors duration-150 hover:bg-gray-200"
    >
      {icon}
    </button>
  );
};

export default IconButton;
