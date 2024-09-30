import React from "react";
import { Link } from "react-router-dom";
// icons
import LogoIcon from "../icons/LogoIcon";
import SendIcon from "../icons/SendIcon";
import ArrowIcon from "../icons/ArrowIcon";

export default function Footer() {
  return (
    <>
      <footer className="mt-5 w-full rounded-2xl bg-black p-14">
        <div className="mx-auto max-w-[1100px] text-white">
          <div>
            <div className="mx-auto text-center">
              <h3>Create Your First Event</h3>
              <p>Start today and bring your first event to life</p>
              <div className="m-3 flex justify-center">
                <button className="flex h-10 w-40 items-center justify-center rounded-3xl border border-black bg-white text-black hover:bg-gray-200">
                  <div className="pr-1">Get Started</div>
                  <ArrowIcon />
                </button>
                <button className="mx-3 h-10 w-40 rounded-[20px] border border-white text-white hover:bg-[#3d3d3d]">
                  <span> Chat with us</span>
                </button>
              </div>
            </div>
          </div>

          <div className="py-20 md:flex">
            <div className="mx-auto w-[370px] space-x-2">
              <h1>STAY CONNECTED</h1>
              <p>
                Sign up for our latest news, software updates and helpful
                resources to promote your events online.
              </p>
              <form className="mx-auto w-full">
                <div className="relative">
                  <input
                    type="email"
                    className="block h-[60px] w-full rounded-[30px] bg-[#201F1F] pl-5 font-[500] text-[#fff] focus:border-blue-500 focus:ring-blue-500"
                    placeholder="Email address..."
                    required
                  />
                  <button
                    type="submit"
                    className="absolute bottom-2.5 end-2.5 h-11 w-11 rounded-full bg-black px-2 py-2"
                  >
                    <SendIcon />
                  </button>
                </div>
              </form>
            </div>

            <div className="sm:mt-7 mx-auto flex w-[370px]  no-underline justify-between">
              <div className="grid">
                <span className=" font-bold">PRODUCT</span>
                <Link className=" no-underline text-white">Home</Link>
                <Link className=" no-underline text-white">How it works</Link>
                <Link className=" no-underline text-white">Benefits</Link>
              </div>

              <div className="grid">
                <span className=" font-bold">LEGAL</span>
                <Link to="" className=" no-underline text-white">
                  Privacy Policy
                </Link>
                <Link className=" no-underline text-white">
                  Terms & Conditions
                </Link>
                <Link className=" no-underline text-white">
                  Services Agreement
                </Link>
              </div>
            </div>
          </div>

          <div className="flex justify-between">
            <LogoIcon />
            <span>© 2024 All Rights Reserved. Planr</span>
          </div>
        </div>
      </footer>
    </>
  );
}
