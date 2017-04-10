using UnityEngine;

namespace Assets.Scripts
{
    public abstract class AICamera : MonoBehaviour
    {
        // Use These Variables to Assign where you want the camera to move
        /// <summary> The x, y, and z of target position. </summary>
        protected Vector3 targetPosition = new Vector3(-3, 2, -5);
        /// <summary> Eular rotation vector. </summary>
        protected Vector3 targetRotation = new Vector3(20, 90, 30);
        /// <summary> Camera move speed. </summary>
        protected float moveSpeed = .5f;

        // DO NOT ALTER THESE VARIABLES
        /// <summary> Reference to the scene's camera. </summary>
        private Camera c;
        /// <summary> Reference to the scene's camera. </summary>
        protected Camera C { get { return c; } }
        /// <summary> Current time for the movement Lerp. </summary>
        private float curMoveTime = 0;
        /// <summary> Current time for the movement Lerp. </summary>
        protected float CurMoveTime { get { return curMoveTime; } }
        /// <summary> The starting point of the Lerp. </summary>
        private Vector3 moveStartPos;
        /// <summary> The starting point of the Lerp. </summary>
        protected Vector3 MoveStartPos { get { return moveStartPos; } }
        /// <summary> The starting rotation of the Lerp. </summary>
        private Quaternion moveStartRot;
        /// <summary> The starting rotation of the Lerp. </summary>
        protected Quaternion MoveStartRot { get { return moveStartRot; } }
        /// <summary> True if the camera is Lerping from one position to another. </summary>
        private bool isMoving = false;
        /// <summary> True if the camera is Lerping from one position to another. </summary>
        public bool IsMoving { get { return isMoving; } }
        public Vector3 TargetPosition { get { return targetPosition; } }
        public Vector3 TargetRotation { get { return targetRotation; } }
        //DO NOT ALTER THESE VARIABLES

        /// <summary> Unity's initialization method. Called on Gameobject instantiation. </summary>
        private void Start()
        {
            targetPosition = new Vector3(-3, 2, -5);
            targetRotation = new Vector3(20, 90, 30);
            moveSpeed = .5f;
            c = GetComponent<Camera>();
            curMoveTime = 0;
            moveStartPos = Vector3.zero;
            moveStartRot = Quaternion.identity;
            isMoving = false;
            try
            {
                Initialize();
            }
            catch (System.Exception e)
            {
                Debug.LogError("ERROR: Crashed in Initialize: " + e.Message);
            }
        }

        // You implement this
        public abstract void Initialize();

        /// <summary> Unity's update method.  Its called once per frame. </summary>
        private void Update()
        {
            // Starts a movement when space bar is pressed
            if (Input.GetKeyDown(KeyCode.Space))
                MoveCamera(targetPosition, targetRotation, moveSpeed, true);
            try
            {
                Run();
            }
            catch (System.Exception e)
            {
                Debug.LogError("ERROR: Crashed in Run: " + e.Message);
            }
            // This call continues the movement if the camera is curently set to move
            if (isMoving)
                MoveCamera(targetPosition, targetRotation, moveSpeed);
        }

        // You implement this
        public abstract void Run();

        /// <summary> Moves the Camera to a target position and target rotation. </summary>
        /// <param name="targetPos"> The position to move to. </param>
        /// <param name="targetRotation"> The rotation to move to. </param>
        /// <param name="speed"> The speed to move at. </param>
        /// <param name="beginMove"> Should be true if this is the start of the Lerp. </param>
        protected void MoveCamera(Vector3 targetPos, Vector3 targetRotation, float speed, bool beginMove = false)
        {
            if (beginMove)
            {
                curMoveTime = 0;
                moveStartPos = transform.position;
                moveStartRot = transform.rotation;
                isMoving = true;
            }
            else
            {
                Quaternion tarRotationQuat = Quaternion.Euler(targetRotation);
                transform.position = Vector3.Lerp(moveStartPos, targetPos, curMoveTime * speed);
                transform.rotation = Quaternion.Slerp(moveStartRot, tarRotationQuat, curMoveTime * speed);
                curMoveTime += Time.deltaTime;
                if (curMoveTime * speed >= 1)
                {
                    transform.position = targetPos;
                    transform.rotation = tarRotationQuat;
                    isMoving = false;
                }
            }

        }

        /// <summary> Returns an array of all Obsticle Boxes in the scene, perimeter walls and floor excluded. </summary>
        /// <returns> All Obsticle Boxes in the scene, perimeter walls and floor excluded. </returns>
        protected GameObject[] getBoundingBoxes()
        {
            GameObject[] g = GameObject.FindGameObjectsWithTag("Obstacle");
            return g;
        }

        /// <summary> Returns an array of all Compy AI creatures. </summary>
        /// <returns> All Compy AI creatures. </returns>
        protected GameObject[] getCompys()
        {
            GameObject[] g = GameObject.FindGameObjectsWithTag("Compy");
            return g;
        }

        /// <summary> Returns a float for the Field Of View for the Camera. </summary>
        /// <returns> The FOV of the camera. </returns>
        protected float getFOV()
        {
            return c.fieldOfView;
        }

        /// <summary> Returns a 3D Vector of the Camera's current position. </summary>
        /// <returns> The camera's current position. </returns>
        protected Vector3 getPosition()
        {
            return transform.position;
        }

        /// <summary> 
        /// Returns a Quaternion that represents the transforms current rotation. (See Unity Reference on Quaternion)
        /// </summary>
        /// <returns> The camera's current rotation. </returns>
        protected Quaternion getRotation()
        {
            return transform.rotation;
        }
    }
}
