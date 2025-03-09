import IconButton from "./Iconbutton";

interface ButtonRowProps {
  interactionHandler: (
    preferences: "liked" | "disliked" | "watch_later" | "not_watched"
  ) => void;
}

const ButtonRow = ({ interactionHandler }: ButtonRowProps) => {
  return (
    <>
      <div className="mt-8 flex w-full max-w-lg justify-between">
        <IconButton
          onClick={() => interactionHandler("liked")}
          icon={
            <svg className="h-8 w-8 fill-current" viewBox="0 0 20 20">
              <path
                d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                clipRule="evenodd"
                fillRule="evenodd"
              ></path>
            </svg>
          }
        />
        <IconButton
          onClick={() => interactionHandler("not_watched")}
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              className="h-8 w-8 fill-current"
            >
              <path
                fill="currentColor"
                d="M17.3 3.3c-.4-.4-1.1-.4-1.6 0l-2.4 2.4a9.6 9.6 0 0 0-3.3-.6c-3.8.1-7.2 2.1-9 5.4c.2.4.5.8.8 1.2c.8 1.1 1.8 2 2.9 2.7L3 16.1c-.4.4-.5 1.1 0 1.6c.4.4 1.1.5 1.6 0L17.3 4.9c.4-.5.4-1.2 0-1.6m-10.6 9l-1.3 1.3c-1.2-.7-2.3-1.7-3.1-2.9C3.5 9 5.1 7.8 7 7.2c-1.3 1.4-1.4 3.6-.3 5.1M10.1 9c-.5-.5-.4-1.3.1-1.8c.5-.4 1.2-.4 1.7 0zm8.2.5c-.5-.7-1.1-1.4-1.8-1.9l-1 1c.8.6 1.5 1.3 2.1 2.2C15.9 13.4 13 15 9.9 15h-.8l-1 1c.7-.1 1.3 0 1.9 0c3.3 0 6.4-1.6 8.3-4.3c.3-.4.5-.8.8-1.2c-.3-.3-.5-.7-.8-1M14 10l-4 4c2.2 0 4-1.8 4-4"
              ></path>
            </svg>
          }
        />
        <IconButton
          onClick={() => interactionHandler("watch_later")}
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-8 w-8 fill-current"
              viewBox="0 0 24 24"
            >
              <path d="M12 2.25l3.09 6.26 6.91 1.005-5 4.87 1.18 6.89L12 17.77l-6.18 3.255 1.18-6.89-5-4.87L8.91 8.51 12 2.25z" />
            </svg>
          }
        />

        <IconButton
          onClick={() => interactionHandler("disliked")}
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-8 w-8 fill-current"
              viewBox="0 0 24 24"
            >
              <path d="M18.364 5.636a1 1 0 0 0-1.414-1.414L12 9.172 7.05 4.222a1 1 0 1 0-1.414 1.414L9.172 12l-4.95 4.95a1 1 0 1 0 1.414 1.414L12 14.828l4.95 4.95a1 1 0 0 0 1.414-1.414L14.828 12l4.95-4.95z" />
            </svg>
          }
        />
      </div>
    </>
  );
};

export default ButtonRow;
