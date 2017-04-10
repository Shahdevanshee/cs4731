using UnityEngine;

namespace Assets.Scripts
{
    public class VisibilityChecker : MonoBehaviour
    {
        /// <summary> The distance constraint for grading. X = lower bound, Y = upper bound. </summary>
        [Tooltip("The distance constraint. X = lower bound, Y = upper bound.")]
        public Vector2 desiredDistance = new Vector2(1, 10);
        /// <summary> The angle constraint for grading. X = lower bound, Y = upper bound. </summary>
        [Tooltip("The angle constraint. X = lower bound, Y = upper bound.")]
        public Vector2 desiredAngle = new Vector2(0, 60);
        /// <summary> Layers to consider during raycast. </summary>
        [Tooltip("Layers to consider during raycast.")]
        public LayerMask RayCastLayers;
        /// <summary> The amount of frames to wait between grabing each test frame. </summary>
        [Tooltip("The amount of frames to wait between grabing each test frame.")]
        public int framesBetweenTest = 50;

        /// <summary> Reference to the camera object. </summary>
        private GameObject myCamera = null;
        /// <summary> The dinos that should be in view. </summary>
        private GameObject[] dinos;
        /// <summary> Timer for waiting inbetween checking visibility. </summary>
        private int currentFrame;

        private void Start()
        {
            myCamera = FindObjectOfType<Camera>().gameObject;
            dinos = GameObject.FindGameObjectsWithTag("Compy");
            currentFrame = 0;
        }

        private void FixedUpdate()
        {
            if (currentFrame++ > framesBetweenTest)
            {
                CheckForDinos();
                currentFrame = 0;
            }
        }

        /// <summary> Grades the current camera frame. </summary>
        private void CheckForDinos()
        {
            float visibleDinos = 0;
            foreach (GameObject ai in dinos)
            {
                // Check if even remotely visible
                if (ai.GetComponentInChildren<Renderer>().isVisible)
                {
                    Vector3 dinoCenter = new Vector3(ai.transform.position.x, ai.transform.position.y + .25f,
                        ai.transform.position.z);
                    Vector3 dinoHead = new Vector3(ai.transform.position.x - .25f, ai.transform.position.y + .25f,
                        ai.transform.position.z);
                    Vector3 dinoTail = new Vector3(ai.transform.position.x - .25f, ai.transform.position.y + .25f,
                        ai.transform.position.z);
                    if (GetVisible(dinoCenter))
                        visibleDinos += GetAllowedViewPoint(dinoCenter);
                    else if (GetVisible(dinoHead))
                        visibleDinos++;
                    else if (GetVisible(dinoTail))
                        visibleDinos++;
                }
            }
            Debug.Log("Dinos visible this frame: " + visibleDinos);
        }

        /// <summary> Checkis if there are any obstructions between the camera and the given point. </summary>
        /// <param name="point"> The point to check. </param>
        /// <returns> True if there is nothing in the way. </returns>
        private bool GetVisible(Vector3 point)
        {
            Vector3 cameraCenter = myCamera.transform.position;
            Vector3 ray = Vector3.Normalize(cameraCenter - point);
            float dist = Vector3.Distance(point, cameraCenter);
            // Check if view obstructed
            if (!Physics.Raycast(point, ray, dist, RayCastLayers))
                return true;
            return false;
        }

        /// <summary> Returns the visibility for the given point based on the current camera distance and angle. </summary>
        /// <param name="point"> The point to check. </param>
        /// <returns> The visibility for the given point. </returns>
        private float GetAllowedViewPoint(Vector3 point)
        {
            Vector3 cameraCenter = myCamera.transform.position;
            Vector3 ray = Vector3.Normalize(cameraCenter - point);
            float dist = Vector3.Distance(point, cameraCenter);
            Vector3 projection = Vector3.ProjectOnPlane(ray, Vector3.up);
            float angle = Vector3.Angle(projection, ray);
            angle %= 360f;
            if ((desiredDistance.x <= dist && dist <= desiredDistance.y) &&
                (desiredAngle.x <= angle && angle <= desiredAngle.y))
            {
                return 1;
            }
            return 0;
        }
    }
}
