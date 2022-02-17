namespace Sys.Data {
    public class Node {
        public Boolean hasValue { get; set; } = false;
        public Object? value { get; set; } = null;
        public Node?[] children { get; set; } = new Node?[0];
        public Node? parent { get; set; } = null;
        public byte? selfInParent { get; set; } = null;

        public Node(Node? parent = null, byte? selfInParent = null) {
            this.parent = parent;
            this.selfInParent = selfInParent;
        }
    }
}