import Cards from "../Components/Cards";
import Welcome from "../Components/Welcome";
import WorkSpace from "../Components/WorkSpace";

const Home = () => {
  return (
    <div className="flex flex-col px-6">
      <Welcome />
      <Cards />
      <WorkSpace />
    </div>
  );
};

export default Home;
