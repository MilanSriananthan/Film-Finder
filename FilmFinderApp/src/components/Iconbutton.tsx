interface IconButtonProps {
  id?: string; // Optional id attribute
  icon: React.ReactNode; // Accepts any valid React node, like an SVG
  onClick?: () => void; // Optional click handler
}

const IconButton = ({ id, icon, onClick }: IconButtonProps) => {
  return (
    <button
      id={id}
      onClick={onClick} // Attach the onClick event
      className="inline-flex h-20 w-20 items-center justify-center rounded-full bg-gray-50 text-black drop-shadow-sm transition-colors duration-150 hover:bg-gray-200"
    >
      {icon}
    </button>
  );
};

export default IconButton;
