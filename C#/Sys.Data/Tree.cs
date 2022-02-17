using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace Sys.Data {
    public class Tree : Node, IEnumerable {
        protected Node? Find(Byte[] key, Boolean withCreate = false) {
            Node? node = this;
            foreach (Byte seg in key.AsEnumerable().Reverse()) {
                if (node.children[seg] is not null) {
                    node = node.children[seg];
                } else if (withCreate is true) {
                    node.children[seg] = new Node(parent = node, selfInParent = seg);
                    node.children[seg].children = new Node?[this.children.Count()];
                    node = node.children[seg];
                } else {
                    node = null;
                    break;
                }
            }
            return node;
        }

        public Object? this[Object key] {
            get {
                Node? node = this.Find((byte[])key);
                if (node is null || node.hasValue is false) { throw new KeyNotFoundException(key.ToString()); }
                return node.value;
            }
            set { }
        }


        public ICollection Keys => throw new NotImplementedException();

        public ICollection Values => throw new NotImplementedException();

        public int Count => throw new NotImplementedException();

        public bool IsSynchronized => throw new NotImplementedException();

        public Object SyncRoot { get; } = new Object();

        public void Add(Object key, Object? value) {
            throw new NotImplementedException();
        }

        public void Clear() {
            throw new NotImplementedException();
        }

        public bool Contains(object key) {
            throw new NotImplementedException();
        }

        public void CopyTo(Array array, int index) {
            throw new NotImplementedException();
        }

        public IEnumerator GetEnumerator() {
            throw new NotImplementedException();
        }
    }
}