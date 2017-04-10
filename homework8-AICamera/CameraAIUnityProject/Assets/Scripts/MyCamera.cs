using UnityEngine;

namespace Assets.Scripts
{
    public class MyCamera : AICamera
    {
        // Use this for initialization
        public override void Initialize()
        {
            Debug.Log("Initialize Called");
        }

        // Run is called once per frame
        public override void Run()
        {
            Debug.Log("Run Called");
        }
    }
}
