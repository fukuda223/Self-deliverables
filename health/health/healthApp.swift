//
//  ContentView.swift
//  health
//
//  Created by 福田恭太郎 on 2024/06/08.
//
import SwiftUI

struct ContentView: View {
    @State private var diseaseSelection = 1
    @State private var improvementSelection = 4
    @State private var isModalPresented = false
    
    var body: some View {
        NavigationView {
            VStack {
                if isModalPresented {
                    ContentView2()
                } else {
                    Text("Hello!\n\nアプリを始める前に\n以下に当てはまるものを選択してください")
                        .font(.largeTitle)
                    
                    Form {
                        Text("該当するものを選択してください")
                        Picker("持病を選択", selection: $diseaseSelection) {
                            Text("").tag(1)
                            Text("高血圧症").tag(2)
                            Text("糖尿病").tag(3)
                            Text("該当なし").tag(4)
                        }
                    }
                    
                    Form {
                        Text("該当するものを選択してください")
                        Picker("食生活での改善したいこと", selection: $improvementSelection) {
                            Text("").tag(5)
                            Text("塩分過多").tag(6)
                            Text("糖質過多").tag(7)
                        }
                    }
                    @AppStorage("Selection1") var  diseaseSelection = 1
                    @AppStorage("Selection2") var improvementSelection = 5
                    
                    Button("次へ") {
                        self.isModalPresented.toggle()
                    }
                    .padding()
                }
            }
            .navigationBarTitle("", displayMode: .inline)
        }
    }
}

struct ContentView2: View {
    var body: some View {
        VStack {
            Text("ようこそ\n\n美味しく健康管理を頑張りましょう")
                .padding()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

//struct ContentViewContainer: View {
    
    //var body: some View {
        //if Selection1 == 1 || 2 || 3 && improvementSelection == 4 || 5 {
                //ContentView2()
                
        //} else {
            //ContentView()
        //}
    //}
//}
