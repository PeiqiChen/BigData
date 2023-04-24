import "../App.css";
import {
    FiMapPin,
    FiMoon,
    FiSearch,
    FiSun,
  } from "react-icons/fi";
import { AiFillCheckSquare } from "react-icons/ai";

function SearchControlLarge() {
    return (
      <div className="hidden md:block">
        <div className="max-w-full bg-white dark:bg-cardColor shadow-sm ml-10 mr-10 rounded-md absolute top-10 right-0 left-0 grid grid-cols-3 gap-4 px-4  mt-6 ">
          <div className="flex align-middle place-items-center border-r border-gray-300 dark:border-gray-700 py-7 flex-grow ">
            <FiSearch className="inline-block  text-primary text-2xl" />
            <input
              className="flex-grow mx-2 h-7 outline-none dark:bg-cardColor dark:text-gray-400 text-black"
              type="text"
              placeholder="Filter by text"
            />
          </div>
          <div className="flex align-middle place-items-center border-r border-gray-300 dark:border-gray-700 py-3 ">
            <FiMapPin className="inline-block  text-primary text-2xl" />
            <input
              className="flex-grow mx-2 h-7 outline-none dark:bg-cardColor dark:text-gray-400 text-black"
              type="text"
              placeholder="Filter by location"
            />
            </div> 
            <div className="justify-between  flex align-middle place-items-center">
            <div className="flex  place-items-center">
              {/* <AiFillCheckSquare className="inline-block text-primary h-6 w-6 text-2xl mr-2 "/>
              <h3 className="inline-block text-lg font-semibold overflow-clip overflow-hidden text-center dark:text-gray-200">
                Full Time Only
              </h3> */}
            </div>
            <button className="bg-primary text-white font-bold text-xl px-8 py-2 rounded-md justify-self-end md:px-5 lg:px-8 hover:bg-primaryLight">
              Search
            </button>
          </div>
        </div>
      </div>
    );
  }
  export default SearchControlLarge;